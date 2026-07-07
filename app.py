import os
import streamlit as st
from langchain_groq import ChatGroq
from pymongo import MongoClient
from langchain_mongodb.agent_toolkit.database import MongoDBDatabase
from langchain_mongodb.agent_toolkit.toolkit import MongoDBDatabaseToolkit
from langchain_mongodb.agent_toolkit import MONGODB_AGENT_SYSTEM_PROMPT
from langchain.agents import create_agent

sidebar_state = "collapsed" if st.session_state.get("connected", False) else "expanded"
st.set_page_config(page_title="QueryNest", layout="centered", initial_sidebar_state=sidebar_state)

if "connected" not in st.session_state:
    st.session_state.connected = False
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    if not st.session_state.connected:
        st.title("Configuration")
        groq_key_input = st.text_input("GROQ_API_KEY", type="password")
        mongo_uri_input = st.text_input("MONGODB_URI", type="password")
        db_name_input = st.text_input("Database Name")
        
        if st.button("Connect"):
            if groq_key_input and mongo_uri_input and db_name_input:
                st.session_state.groq_api_key = groq_key_input
                st.session_state.mongodb_uri = mongo_uri_input
                st.session_state.db_name = db_name_input
                st.session_state.connected = True
                st.session_state.messages.append({"role": "assistant", "content": "How can I help you today?"})
                st.rerun()
            else:
                st.error("Please fill all fields")
    else:
        st.success("Connected to Database")
        if st.button("Disconnect"):
            st.session_state.connected = False
            st.session_state.messages = []
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Message QueryNest..."):
    if not st.session_state.connected:
        st.error("Please configure API keys and Connect in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            llm = ChatGroq(
                model="openai/gpt-oss-20b",
                api_key=st.session_state.groq_api_key,
                max_tokens=2048,
                reasoning_effort="low",
            )
            
            client = MongoClient(st.session_state.mongodb_uri)
            mongo_db = MongoDBDatabase(client=client, database=st.session_state.db_name)
            toolkit = MongoDBDatabaseToolkit(db=mongo_db, llm=llm)
            
            system_message = MONGODB_AGENT_SYSTEM_PROMPT.format(top_k=5)
            system_message += """

CRITICAL TOOL USAGE INSTRUCTIONS:
1. COLLECTION NAMES: ALWAYS verify exact collection names using the appropriate tool before querying. NEVER guess (e.g., check for 'playlists' if asked about 'playlist').
2. TOOL NAMES: When calling tools, use EXACTLY the tool name provided. DO NOT add punctuation, suffixes, or apostrophes (e.g., NEVER use 'mongodb_query_checker's' - use the exact tool name without quotes).
3. ERROR RECOVERY: If a tool returns an error or you get a tool validation error, read the error and fix your next tool call. DO NOT repeat the same mistake.
4. Always construct correct MongoDB query syntax."""
            agent = create_agent(
                model=llm,
                tools=toolkit.get_tools(),
                system_prompt=system_message,
            )
            
            with st.status("Agent thinking...", expanded=True) as status:
                final_response = None
                for chunk in agent.stream(
                    {
                        "messages": [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    },
                    stream_mode="updates"
                ):
                    for node, values in chunk.items():
                        if node == "agent" or node == "model":
                            msg = values["messages"][-1]
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                for tool_call in msg.tool_calls:
                                    st.write(f"🔧 **Tool Call:** `{tool_call['name']}`")
                                    with st.expander("Tool Arguments"):
                                        st.json(tool_call['args'])
                        elif node == "tools":
                            msg = values["messages"][-1]
                            st.write(f"✅ **Tool Result:** `{msg.name}`")
                            with st.expander("Tool Output"):
                                st.write(msg.content)
                        
                        final_response = values
                
                status.update(label="Response Ready!", state="complete", expanded=False)
            
            answer = final_response["messages"][-1].content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")