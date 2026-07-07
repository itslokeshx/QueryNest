import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pymongo import MongoClient
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MONGODB_URI=os.getenv("MONGODB_URI")


llm=ChatGroq(model="openai/gpt-oss-20b",api_key=GROQ_API_KEY,verbose=True)
client = MongoClient(MONGODB_URI)
db =client["soulsync"]
users=db["users"]

mongo_db=MongoDBDatabase(client=client,database="soulsync")

toolkit=MongoDBDatabaseToolkit(db=mongo_db,llm=llm)

print(toolkit.get_tools())