AI Manufacturing Copilot

An AI-powered manufacturing analytics assistant that combines RAG (Retrieval-Augmented Generation), LLMs, and MongoDB machine analytics to analyze industrial operations, downtime events, and OEE performance using natural language queries.

🚀 Project Overview

Modern manufacturing industries generate massive amounts of machine and operational data every day.

However, traditional dashboards only display metrics and charts — they rarely explain:

Why downtime occurred
What caused OEE losses
Which machine affected production
How operational efficiency can improve

This project aims to solve that problem by building an AI Manufacturing Copilot capable of understanding industrial data and generating intelligent operational insights.

🧠 Key Features
✅ AI-Powered Manufacturing Assistant

Ask questions in natural language such as:

“Why did Machine DEMO_BD_4 experience high downtime?”
“Explain today’s OEE loss.”
“Tell me about the company and manufacturing workflow.”

The system generates contextual AI responses using:

industrial machine analytics
retrieved document context
manufacturing rules
LLM reasoning
✅ RAG-Based Document Intelligence

The system supports:

Company PDFs
Industrial manuals
SOP documents
Industry 4.0 documentation

Using:

document chunking
embeddings
vector search
semantic retrieval

This enables accurate industrial Q&A with reduced hallucinations.

✅ MongoDB Machine Analytics

The system analyzes structured industrial machine data stored in MongoDB.

Supported Metrics
OEE
Availability
Performance
Quality
Downtime events
Shift analytics
Hourly production
Breakdown reasons
✅ AI-Generated Operational Insights

The AI can:

Explain downtime causes
Analyze performance losses
Detect operational bottlenecks
Suggest corrective actions
Interpret manufacturing metrics

🏗️ **System Architecture**
User Question
      ↓
Intent Router
      ↓
 ┌───────────────────────┐
 │ RAG Pipeline          │
 │ Company Manuals/PDFs  │
 └───────────────────────┘
             OR
 ┌───────────────────────┐
 │ MongoDB Machine Data  │
 │ OEE + Downtime Data   │
 └───────────────────────┘
      ↓
Prompt Engineering Layer
      ↓
Large Language Model
      ↓
AI-generated Insights

⚙️ **Tech Stack**
Frontend
Streamlit
Backend
Python
Database
MongoDB
AI Stack
Large Language Models (LLMs)
RAG Pipeline
Embeddings
Vector Search
Prompt Engineering
Manufacturing Concepts
OEE Analytics
Downtime Analysis
Industry 4.0
Industrial Automation
📂 Project Structure
AI-Manufacturing-Copilot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── manuals/
│   ├── company_docs/
│
├── rag/
│   ├── embeddings.py
│   ├── retriever.py
│   ├── vector_store.py
│
├── analytics/
│   ├── oee_analysis.py
│   ├── downtime_analysis.py
│
├── database/
│   ├── mongodb_connection.py
│
└── screenshots/
📊 MongoDB Manufacturing Data Model

The analytics system follows a real manufacturing hierarchy:

Organization
   → Plant
      → Production Line
         → Machine

Each machine document contains:

daily analytics
monthly analytics
OEE metrics
downtime summaries
shift-wise production
hourly metrics
breakdown events
💡 Example Queries
Manufacturing Analytics
Why did OEE decrease today?
Which machine had the highest downtime?
Explain performance losses.
Show breakdown trends.
Document Intelligence
Explain the machine startup procedure.
Tell me about the company.
What are the Industry 4.0 guidelines?
🔥 Future Improvements

Planned upgrades include:

Predictive Maintenance
Real-time anomaly detection
AI maintenance recommendations
Production forecasting
Multi-plant analytics
Live IoT integration
Advanced dashboards
Autonomous industrial copilot !

chatbot UI
architecture diagram
downtime analysis results
MongoDB analytics
▶️ Installation
Clone Repository
git clone https://github.com/your-username/AI-Manufacturing-Copilot.git
Install Dependencies
pip install -r requirements.txt
Run Application
streamlit run app.py
🌍 Vision

The goal of this project is to explore how AI systems can move beyond traditional chatbots into real industrial intelligence platforms capable of:

operational reasoning
manufacturing analytics
downtime investigation
intelligent decision support
👨‍💻 Author
Deepasruthi.R

AI / ML Engineer
Focused on:

Generative AI
RAG Systems
Industrial AI
Manufacturing Analytics
LLM Applications
⭐ If You Found This Interesting

Feel free to:

Star the repository
Connect on LinkedIn
Share feedback
Suggest improvements
