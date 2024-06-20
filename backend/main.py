from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3
import os

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt','pdf','docx','md'}
DATABASE = 'threads.db'

load_dotenv()

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, origins=["http://localhost:5173"], methods=['GET', 'POST', 'DELETE'])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE)
    return db 

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() 

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

@app.route('/api/files/', methods=['GET', 'POST', 'DELETE'])
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

    if request.method == 'DELETE':
        id = request.args.get('id')
        if not id:
            return jsonify({
                'status': 'error',
                'message': 'Failed to retrieve file ID'
            }), 401

        file = client.files.delete(id)
        return jsonify({
            'status': 'success',
            'message': 'Successfully deleted file'
        }), 200

@app.route('/api/threads/', methods=['GET', 'POST', 'DELETE'])
def threads_api():
    if request.method == 'POST':
        name = request.args.get('name')
        vstore_id = request.args.get('vstore_id')

        thread = client.beta.threads.create()

        db = get_db()
        cur = db.cursor() 

        try: 
            cur.execute(f"""
                INSERT INTO thread VALUES
                    ("{thread.id}", "{name}", "{vstore_id}")
            """)
            db.commit() 
            return "Thread created successfully", 200 
        except Exception as e:
            db.rollback() 
            return str(e), 500 
        finally:
            cur.close() 
    
    if request.method == 'GET':
        db = get_db()
        cur = db.cursor() 

        try: 
            cur.execute("SELECT * FROM thread")
            threads = cur.fetchall() 

            threads_list = []
            for thread in threads:
                thread_dict = {
                    'id': thread[0],
                    'name': thread[1],
                    'vstore_id': thread[2]
                }
                threads_list.append(thread_dict)

            return jsonify(threads_list), 200
        except Exception as e:
            db.rollback() 
            return str(e), 500 
        finally:
            cur.close()

    if request.method == 'DELETE':
        id = request.args.get('id')
        db = get_db()
        cur = db.cursor() 

        try:
            cur.execute(f"DELETE FROM thread WHERE id = \"{id}\"")
            db.commit()
            return "Successfully deleted thread", 200 
        except Exception as e:
            db.rollback() 
            return str(e), 500 
        finally:
            cur.close()

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

    try:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("CREATE TABLE thread(id, name, vstore_id)")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
    
    app.run(host='0.0.0.0', debug=True)
