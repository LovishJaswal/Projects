# 🚀 VibeForge

> **Helping Open Source Move Faster.**

VibeForge is an AI-powered GitHub Issue Analyzer that helps developers understand new issues and discover semantically related issues using LLMs, embeddings, and vector search.

Unlike traditional keyword search, VibeForge understands the **meaning** behind an issue.

---

# ✨ Features

- 📦 Index any public GitHub repository
- 📝 AI-powered issue analysis
- 🔍 Semantic search for related issues
- 🧠 Embedding-based retrieval using ChromaDB
- 🤖 LLM explanations for retrieved issues

---

# 🛠️ Tech Stack

- **Backend:** Python
- **LLM:** Google Gemini 2.5 Flash Lite
- **Embeddings:** sentence-transformers/all-mpnet-base-v2
- **Vector Database:** ChromaDB
- **Frameworks:** LangChain, Gradio
- **API:** GitHub REST API

---

# ⚙️ How It Works

```
GitHub Repository
        │
        ▼
 Fetch GitHub Issues
        │
        ▼
 Process Issue Data
        │
        ▼
 Create Documents
        │
        ▼
 Generate Embeddings
        │
        ▼
 Store in ChromaDB
        │
        ▼
 Repository Indexed
        │
        ▼
 User Enters Issue
        │
        ▼
   AI Issue Analysis
        │
        ▼
 Semantic Search
        │
        ▼
 Related Issues
```

---

# 📂 Repository Structure

```
VibeForge/

├── data/
├── src/
│   ├── github_client.py
│   ├── process_issues.py
│   ├── create_documents.py
│   ├── embeddings.py
│   ├── vector_db.py
│   ├── find_similar_issues.py
│   ├── llm_issue_analyzer.py
│   └── llm_related_issues.py
│
├── main.py
├── pyproject.toml
└── README.md
```

---

# 🚀 Installation

```bash
git clone <repository-url>

cd VibeForge

uv sync

uv run main.py
```

---

# 🔮 Future Improvements

- Local LLM support
- Private repository support
- Automatic issue labeling
- Pull request analysis
- Multi-repository search
- Repository intelligence dashboard

---

