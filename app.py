import os
import streamlit as st
from langchain_groq import ChatGroq
from pymongo import MongoClient
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit
from langchain_mongodb.agent_toolkit import MONGODB_AGENT_SYSTEM_PROMPT
from langchain.agents import create_agent

st.set_page_config(page_title="QueryNest", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #121212;
        color: #e0e0e0;
    }
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }
    .stTextInput>div>div>input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #444;
    }
    .stTextInput>div>div>input:focus {
        border-color: #bb86fc;
        box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Configuration")
    groq_api_key = st.text_input("GROQ_API_KEY", type="password")
    mongodb_uri = st.text_input("MONGODB_URI", type="password")
    db_name = st.text_input("Database Name")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message QueryNest..."):
    if not groq_api_key or not mongodb_uri:
        st.error("Please configure API keys in the sidebar")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                llm = ChatGroq(
                    model="openai/gpt-oss-20b",
                    api_key=groq_api_key,
                    max_tokens=2048,
                    reasoning_effort="low",
                )
                
                client = MongoClient(mongodb_uri)
                mongo_db = MongoDBDatabase(client=client, database=db_name)
                toolkit = MongoDBDatabaseToolkit(db=mongo_db, llm=llm)
                
                system_message = MONGODB_AGENT_SYSTEM_PROMPT.format(top_k=5)
                agent = create_agent(
                    model=llm,
                    tools=toolkit.get_tools(),
                    system_prompt=system_message,
                )
                
                response = agent.invoke({
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                })
                
                answer = response["messages"][-1].content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")