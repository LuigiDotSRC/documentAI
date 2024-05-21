from openai import OpenAI, AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override
import os 

load_dotenv()

# set OPENAI_API_KEY env variable
print(os.getenv("OPENAI_API_KEY"))
client = OpenAI() 

assistant = client.beta.assistants.create(
    name="Document Scanner Assistant",
    instructions="You are given access to user documents. Use the data in the documents to answer user queries.",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
)
