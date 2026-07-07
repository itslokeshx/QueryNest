import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pymongo import MongoClient
load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
MONGODB_URI=os.getenv("MONGODB_URI")

llm=ChatGroq(model="openai/gpt-oss-20b",api_key=GROQ_API_KEY,verbose=True)
client = MongoClient(MONGODB_URI)
db =client["soulsync"]
users=db["users"]
print(users.find_one())
