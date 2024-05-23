from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def retrieve_assistant(id):
    return client.beta.assistants.retrieve(id)

# Associate a new vector store with an assistant 
def assoc_vector_store(assistant_id, vstore_id):
    assoc_vstore_ids = retrieve_assistant("asst_aO4UpBhpU9E777BHlym1glyb").tool_resources.file_search.vector_store_ids

    return client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": assoc_vstore_ids.append(vstore_id)}},
    )

# Remove a vector store from an assistant 
def rm_vector_store(assistant_id, vstore_id):
    assoc_vstore_ids = retrieve_assistant("asst_aO4UpBhpU9E777BHlym1glyb").tool_resources.file_search.vector_store_ids

    return client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": assoc_vstore_ids.remove(vstore_id)}},
    )

