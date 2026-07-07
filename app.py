import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pymongo import MongoClient
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit
from langchain_mongodb.agent_toolkit import MONGODB_AGENT_SYSTEM_PROMPT
from langchain.agents import create_agent


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    max_tokens=2048,      
    reasoning_effort="low", 
)

client = MongoClient(MONGODB_URI)
db = client["soulsync"]
users = db["users"]

mongo_db = MongoDBDatabase(client=client, database="soulsync")
toolkit = MongoDBDatabaseToolkit(db=mongo_db, llm=llm)

system_message = MONGODB_AGENT_SYSTEM_PROMPT.format(top_k=5)
agent = create_agent(
    model=llm,
    tools=toolkit.get_tools(),
    system_prompt=system_message,
)

query = "how many users in the db!?"

response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })
print("\nFinal answer:", response["messages"][-1].content)

 