<div align="center">

# QueryNest
**A Practical Agentic Interface for MongoDB**

<p align="center">
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"></a>
  <a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/Orchestration-LangChain-1C3C3C?style=for-the-badge&logo=langchain" alt="LangChain"></a>
  <a href="https://www.mongodb.com/"><img src="https://img.shields.io/badge/Database-MongoDB-4EA94B?style=for-the-badge&logo=mongodb" alt="MongoDB"></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/LLM-Groq-f55036?style=for-the-badge" alt="Groq"></a>
</p>

> *QueryNest is a continuous work in progress, serving as a practical template and learning ground for building, debugging, and understanding AI agents.*

</div>

---

## 📖 Overview

QueryNest is a simple, conversational web interface that allows users to interact with a MongoDB database using natural language. Built as an open practice ground for understanding **agentic architectures**, it bridges the gap between raw database logic and human conversation. It's designed to be a helpful, humble starting point for anyone looking to build robust database-querying agents without over-engineering.

<br>

## 🛠️ Architecture & System Design (SD)

QueryNest follows a standard **ReAct (Reasoning and Acting)** agent pattern implemented via LangGraph. 

Here is a high-level overview of the System Design and Data Flow. This cycle repeats until the agent has successfully answered the user's query:

```mermaid
graph TD
    classDef user fill:#2d2d2d,stroke:#bb86fc,stroke-width:2px,color:#fff;
    classDef agent fill:#1e1e1e,stroke:#4EA94B,stroke-width:2px,color:#fff;
    classDef db fill:#1C3C3C,stroke:#4EA94B,stroke-width:2px,color:#fff;

    A((👤 User)):::user -->|Enters Query| B[🖥️ Streamlit UI]:::user
    B -->|Context & Credentials| C{🧠 LangGraph Agent}:::agent
    
    subgraph Agentic Loop
        C -->|1. Reason & Plan| C
        C -->|2. Tool: List Collections| D[(🍃 MongoDB)]:::db
        D -.->|Available Schema| C
        C -->|3. Tool: Query Checker| E[🛡️ Validation]:::agent
        E -.->|Validated Aggregation Pipeline| C
        C -->|4. Tool: Execute Query| D
        D -.->|Raw JSON Results| C
    end
    
    C -->|5. Synthesize Context| B
    B -->|Streams Thoughts & Final Answer| A
```

### 🧩 Core Components
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | `Streamlit` | Handles user inputs, securely stores URI/API keys in session state, and natively streams the agent's internal thought process in real-time. |
| **Agent Core** | `LangGraph` | Orchestrates the flow. It parses the user query, decides which tool to use, and recursively evaluates the tool's output. |
| **Tools** | `Langchain Toolkit` | Includes **List Collections** (schema check), **Query Checker** (syntax validation), and **Query Executor** (safely runs the pipeline). |
| **LLM Engine** | `Groq` | Provides the lightning-fast reasoning layer (e.g., `gpt-oss-20b` or `Llama3`) to translate plain English into valid MongoDB pipelines. |

<br>

## 🚀 Getting Started

### 📋 Prerequisites
Before you begin, ensure you have the following:
- **Python 3.9+** installed on your system.
- A **Groq API Key** (You can generate one at [console.groq.com](https://console.groq.com)).
- A **MongoDB Cluster / Database URI** (e.g., via MongoDB Atlas).

### ⚙️ Setup Instructions

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/QueryNest.git
cd QueryNest
```

**2. Set up a virtual environment (Recommended):**
Keep your dependencies isolated to avoid conflicts.
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

**3. Install the dependencies:**
Install all required packages cleanly via the provided `requirements.txt`.
```bash
pip install -r requirements.txt
```
*(Note: Streaming logic is handled safely and natively in the main thread via Streamlit's `st.status`, avoiding common threading issues in LangChain callbacks).*

**4. Run the application:**
```bash
streamlit run app.py
```

<br>

## 💡 Usage Flow

1. 🔐 **Configure:** Upon launching the UI, open the sidebar and securely input your `GROQ_API_KEY`, your `MONGODB_URI`, and the target `Database Name`.
2. 🔌 **Connect:** Click **Connect**. The app will initialize the LangChain MongoDB toolkit and establish a secure connection.
3. 💬 **Chat:** Start asking questions about your data! Try prompts like:
   - *"How many users do we have in total?"*
   - *"List the top 5 users based on their listening time."*
4. 🔍 **Observe the Agent:** Click the **"Agent thinking..."** dropdown in the chat to look under the hood. You'll see exactly how the model reasons, which tools it selects, and the raw output it receives from MongoDB before giving you the final human-readable answer.

---
<div align="center">
  <sub>Built for the love of AI engineering and exploring agentic logic.</sub>
</div>
