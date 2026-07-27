# 📊 Autonomous Text-to-SQL Business Intelligence Suite

An enterprise-grade, conversational AI data analytics application that translates natural business language queries into precise, executable SQLite queries. Powered by ultra-low latency LLMs via the **Groq API** and built using **Streamlit**, this suite provides interactive management layers and dynamic visual data analytics reporting on the fly.

---

## ✨ Features
*   **Conversational Data Discovery:** Query relational database tables using plain conversational English.
*   **Ultra-Low Latency Inference:** Integrated with the `llama-3.3-70b-versatile` model via Groq's high-speed LPU architecture.
*   **Administrative Management Dashboard:** Tab-separated design allowing users to seamlessly view, add, or delete active database entries.
*   **Live Financial Analytics Charts:** Instant real-time aggregations of data visualizations (salary break-downs and department averages) using dynamic bar charts.
*   **Security First Core:** Fully decoupled environment variable systems (`.env`) to enforce data perimeter safety and block secret exposure.
*   **Backup Utility:** Built-in table compilation exporter allows instant downloads of the data matrix into standard CSV spreadsheets.

---

## 🛠️ Technology Stack & Frameworks
*   **Language Engine:** Python 3
*   **AI Framework Orchestration:** LangChain Core
*   **LLM Inference Core:** Groq API Cloud Client Layer (`langchain-groq`)
*   **Database Engine:** SQLite (Embedded relational structure)
*   **Frontend Presentation Interface:** Streamlit Framework
*   **Data Aggregation Analytics:** Pandas Toolkit

---

## 📁 System Architecture Directory Layout
```text
ai_sql_agent/
│
├── .env                # Hidden private key configuration profiles (git-ignored)
├── .gitignore          # File layout configurations protecting systemic leak paths
├── README.md           # Professional technical project documentation mapping
├── agent.py            # Natural Language Processing extraction & Text-to-SQL logic
├── app.py              # Visual presentation UI layout & application dashboard
├── company.db          # Embedded active SQLite binary file system
└── db_setup.py         # Seed deployment module constructing schema tables
```

---

## 🚀 Setup, Installation & Local Deployment

### 1. Pre-requisite Repository Isolation
Clone or download the project files into your target workspace environment directory:
```bash
cd ai_sql_agent
```

### 2. Dependency Infrastructure Assembly
Deploy the environmental dependencies inside your workspace shell terminal:
```bash
pip install langchain-groq langchain-core streamlit pandas python-dotenv
```

### 3. API Perimeter Configuration
Build a `.env` deployment profile directly in your root workspace path:
```text
GROQ_API_KEY=gsk_your_actual_private_api_key_string_here
```

### 4. Database Table Initialization
Compile the script once to generate your local `company.db` engine and insert initial mockup data rows:
```bash
python db_setup.py
```

### 5. Launching the Web Interface Suite
Fire up your localized Streamlit rendering engine to start asking questions in your web browser:
```bash
streamlit run app.py
```

---

## 🔒 Security & Safe Injection Audits
*   **Read-Only Safe Architecture:** The application logic separates data query tasks safely away from active write tables.
*   **Prompt Restrictive Containment:** System definitions restrict processing commands from executing unwanted modifications (`DROP`, `ALTER`, `UPDATE`).
