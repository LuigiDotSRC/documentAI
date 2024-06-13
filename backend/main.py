from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt','pdf','docx','md'}

load_dotenv()

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins=["http://localhost:5173"], methods=['GET', 'POST', 'DELETE'])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/vector_stores/', methods=['GET', 'POST', 'DELETE'])
def vector_stores_api():
    if request.method == 'GET':
        id = request.args.get('id')

        if id:
            v_store = client.beta.vector_stores.retrieve(vector_store_id=id)
            files = client.beta.vector_stores.files.list(vector_store_id=id)

            return jsonify({
                'name': v_store.name,
                'files': [{'id': file.id, 'bytes': file.usage_bytes} for file in files]
            })
            

        call = client.beta.vector_stores.list().data
        response = []
        for v_store in call:
            response.append(
                {
                    'id': v_store.id,
                    'name': v_store.name,
                    'num_files': v_store.file_counts.completed,
                    'bytes': v_store.usage_bytes
                }
            )
        return jsonify(response)
    
    if request.method == 'POST':
        name = request.args.get('name')

        if not name: 
            return jsonify({
                'status': 'error',
                'message': 'Vector store name required'
            }), 400

        client.beta.vector_stores.create(
            name=name
        )
        return jsonify({
            'status': 'success',
            'message': 'Successfully created vector store'
        }), 200
    
    if request.method == 'DELETE':
        id = request.args.get('id')
        
        if not id:
            return jsonify({
                'status': 'error',
                'message': 'Vector store ID required'
            }), 400
        
        client.beta.vector_stores.delete(id)
        return jsonify({
            'status': 'success',
            'message': 'Successfully deleted vector store'
        }), 200

@app.route('/api/files/', methods=['GET', 'POST'])
def files_api():
    if request.method == 'GET':
        id = request.args.get('id')
        if not id:
            return jsonify({
                'status': 'error',
                'message': 'Failed to retrieve file ID'
            }), 401

        file = client.files.retrieve(id)
        return jsonify({
            'id': file.id,
            'filename': file.filename,
            'bytes': file.bytes,
            'created_at': file.created_at,
        }), 200

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'File not recieved'
            }), 400 
        
        file = request.files['file']

        if file.filename == '': 
            return jsonify({
                'status': 'error',
                'message': 'Bad file name'
            }), 400 
        
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Bad file type'
            }), 400 

        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        try:
            with open(file_path, "rb") as file_stream:
                openai_file = [file_stream]
                file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=request.form.get('vstore_id'),
                    files=openai_file
                )

            return jsonify({
                'status': 'success',
                'message': 'File uploaded successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'{str(e)}'
            }), 200
        finally:
            os.remove(file_path)
            file.close()

# TODO: REFACTOR API ROUTES BELOW FOR PROPER INTERACTION WITH FRONTEND
# TODO: REMOVE FLASK TEMPLATES (NO LONGER NEEDED W/ SVELTE FRONTEND)

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
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if len(client.beta.assistants.list().data) < 1:
        client.beta.assistants.create(
            name="DocAI Reader",
            instructions="You are an AI file assistant. Answer user queries based on the files provided.",
            tools=[{"type": "file_search"}],
            model="gpt-3.5-turbo"
        )

    app.run(host='0.0.0.0', debug=True)
