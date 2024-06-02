from flask import Flask, render_template, flash, request, redirect, url_for, CORS
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt','pdf','docx','md'}

load_dotenv()

app = Flask(__name__) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        # create a new thread, redirect to conversation page
        thread_id = client.beta.threads.create().id
        return redirect(url_for('conversation', thread_id=thread_id))

    return render_template(
        'index.html', 
        data={
            'assistants': client.beta.assistants.list().data,
            'vector_stores': client.beta.vector_stores.list().data,
        }
    )

@app.route('/upld', methods=['GET','POST'])
def upload_file():
    vstore_id = request.args.get('vstore_id')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Process file for OpenAI Vector Store
            file_paths = [os.path.join(app.config['UPLOAD_FOLDER'], filename)]
            file_streams = [open(path, "rb") for path in file_paths]
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vstore_id, files=file_streams
            )
            
            return redirect(url_for('upload_file', vstore_id=vstore_id))

    return render_template(
        'upload_file.html',
        data={
            'vector_store_id': vstore_id,
            'files': client.beta.vector_stores.files.list(vector_store_id=vstore_id),
        }
    )

@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    thread_id = request.args.get('thread_id')

    # load sample vstore, assistant
    vstore_id = 'vs_Xmcc3tZ5tSBfsrd3iorp9ahh'
    assistant_id = 'asst_aO4UpBhpU9E777BHlym1glyb'

    client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search":{"vector_store_ids": [vstore_id]}},
    )

    avail_files = []
    attatchments = []

    for file in client.beta.vector_stores.files.list(vector_store_id=vstore_id).data:
        avail_files.append(file.id)
        attatchments.append(
            { "file_id": file.id, "tools": [{"type": "file_search"}]}
        )

    if request.method == 'POST':
        # upload a new message, await ai response
        usermsg = request.form['message']
        thread_message = client.beta.threads.messages.create(
            thread_id,
            role="user",
            content=usermsg,
            attachments=attatchments
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id, assistant_id=assistant_id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

        return redirect(url_for('conversation', thread_id=thread_id))



    return render_template(
        'conversation.html',
        data={
            'thread_id': thread_id,
            'files': avail_files,
            'messages': client.beta.threads.messages.list(thread_id),
        }
    )

if __name__ == '__main__':
    if len(client.beta.assistants.list().data) < 1:
        client.beta.assistants.create(
            name="DocAI Reader",
            instructions="You are an AI file assistant. Answer user queries based on the files provided.",
            tools=[{"type": "file_search"}],
            model="gpt-3.5-turbo"
        )

    app.run(host='0.0.0.0', debug=True)

