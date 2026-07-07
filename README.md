# 🦜 QueryNest

**QueryNest** is an intelligent, conversational web application that allows you to chat directly with your MongoDB databases using natural language. Built with Streamlit, LangChain, and powered by Groq's blazing-fast LLMs, it transforms complex database queries into simple conversations.

![QueryNest UI preview](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)

## ✨ Features

- **Conversational Interface:** Ask questions about your data in plain English. No need to write complex MongoDB Aggregation pipelines manually.
- **Real-Time Agent Thoughts:** Watch the AI's reasoning process unfold in real-time. The "Agent thinking..." expander shows you exactly what tools are being called and what data is retrieved from the database.
- **Secure Configuration:** Your MongoDB URI and Groq API Key are entered securely through the sidebar and are kept strictly within your active session state.
- **Dynamic Connection:** Seamlessly connect and disconnect from different databases without restarting the application.
- **Sleek Dark Mode UI:** Custom CSS implementation provides a gorgeous, distraction-free dark mode interface right out of the box.

## 🚀 Getting Started

### Prerequisites

You will need the following installed and set up:
- Python 3.9+
- A Groq API Key (get one at [console.groq.com](https://console.groq.com))
- A MongoDB cluster/database URI (e.g., MongoDB Atlas)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/QueryNest.git
   cd QueryNest
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   Make sure you have the required packages installed:
   ```bash
   pip install streamlit langchain langchain-groq langchain-mongodb pymongo
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 💡 How to Use

1. **Configure:** Open the sidebar and enter your `GROQ_API_KEY`, your `MONGODB_URI`, and the specific `Database Name` you want to query.
2. **Connect:** Click the "Connect" button. The app will initialize the LangChain MongoDB toolkit and establish a connection.
3. **Chat:** Type your questions into the chat input! Try prompts like:
   - *"How many users are in the database?"*
   - *"List the top 5 users sorted by listening time."*
   - *"What collections do we have available?"*
4. **Inspect:** Click on the "Agent thinking..." dropdown to see the exact MongoDB queries generated and executed by the AI.

## 🧠 Under the Hood

QueryNest utilizes the modern `create_agent` architecture (powered by LangGraph) from LangChain. It uses the `MongoDBDatabaseToolkit` to automatically detect collections and execute secure aggregation pipelines.

The agent's system prompt ensures strict adherence to aggregation queries (`db.collection.aggregate(...)`), preventing unsupported query types and ensuring high reliability when conversing with your database.

---
*Built with ❤️ for AI engineering and seamless database interactions.*
