from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add_file(vstore_id, file_path):
    file_stream = open(file_path, "rb")
    return client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vstore_id, files=file_stream
    )

