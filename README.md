# 🚀 VibeForge

> **Helping Open Source Move Faster.**

VibeForge is an AI-powered GitHub Issue Analyzer that helps developers understand new issues, discover semantically similar issues, and identify potential duplicates using Large Language Models (LLMs), embeddings, and vector search.

Unlike traditional keyword search, VibeForge understands the *meaning* behind an issue.

---

# 📖 Table of Contents

- Introduction
- The Problem
- Why VibeForge?
- What We Are Building
- Features
- How It Works
- Architecture
- Internal Working
- Tech Stack
- Why These Technologies?
- Project Workflow
- Repository Structure
- Installation
- Future Improvements
- License

---

# Introduction

Open-source repositories receive hundreds or even thousands of GitHub issues.

Many of them describe the exact same problem, but using different wording.

For example,

> "FastAPI crashes while parsing aliases."

and

> "Application fails when using field aliases."

Both may refer to the exact same bug.

Unfortunately, GitHub's built-in search primarily relies on keyword matching.

That means developers often create duplicate issues simply because they cannot find existing ones.

VibeForge solves this problem using semantic search.

Instead of matching words, it understands the meaning behind an issue.

---

# The Problem

As repositories grow, issue management becomes increasingly difficult.

Some common problems include:

- Duplicate issues
- Different wording for the same bug
- Large issue backlog
- Difficult issue discovery
- Time wasted triaging issues
- Inconsistent issue labeling
- Manual duplicate detection

Maintainers often spend valuable time reviewing issues that already exist.

This slows down development and creates unnecessary noise.

---

# Why VibeForge?

Traditional search answers:

> **"Do these issues contain similar words?"**

VibeForge answers:

> **"Do these issues describe the same problem?"**

That difference is the foundation of semantic search.

Instead of searching text literally, VibeForge searches meaning.

---

# What We Are Building

The long-term vision of VibeForge is an AI-powered repository intelligence platform.

The first milestone (MVP) focuses on one core problem:

> **AI-powered GitHub Issue Analysis**

Given a public GitHub repository, VibeForge can:

- Fetch repository issues
- Build a semantic knowledge base
- Analyze new issues
- Find similar historical issues
- Detect likely duplicates

This MVP serves as the foundation for future repository intelligence features.

---

# Features

## Repository Indexing

- Fetches GitHub Issues
- Supports pagination
- Stores raw issue data
- Removes pull requests
- Processes issue metadata

---

## Issue Analysis

Uses an LLM to analyze:

- Summary
- Severity
- Category
- Possible root cause
- Suggested labels
- Recommended next step

---

## Duplicate Detection

Instead of searching keywords,

VibeForge searches for semantic similarity.

Given a new issue,

it retrieves the most relevant historical issues and asks an LLM whether they are likely duplicates.

---

# How It Works

```
                    User
                      │
                      ▼
            Enter Repository Name
                      │
                      ▼
              Fetch GitHub Issues
                      │
                      ▼
            Process Raw GitHub Data
                      │
                      ▼
             Create LangChain Documents
                      │
                      ▼
             Generate Text Embeddings
                      │
                      ▼
             Store in Chroma Database
                      │
                      ▼
                Repository Indexed
                      │
                      ▼
               User Enters New Issue
                      │
          ┌───────────┴────────────┐
          ▼                        ▼
 Issue Analysis             Similarity Search
          │                        │
          ▼                        ▼
      Gemini LLM           Chroma Vector Search
                                   │
                                   ▼
                          Top Similar Issues
                                   │
                                   ▼
                         Duplicate Detection LLM
                                   │
                                   ▼
                               Final Result
```

---

# Internal Working

## Step 1 — Fetch Issues

The application fetches all GitHub Issues using the GitHub REST API.

Pagination is handled automatically until every issue has been downloaded.

Pull Requests are ignored because they are not GitHub Issues.

The fetched data is stored locally.

---

## Step 2 — Process Issues

The raw GitHub response contains many unnecessary fields.

The data is cleaned and converted into a smaller format containing information such as:

- Issue Number
- Title
- Description
- Labels
- State
- URL

---

## Step 3 — Create Documents

Every issue becomes a LangChain Document.

Example:

```
Title:
FastAPI crashes while parsing aliases

Description:
Application crashes after upgrading...
```

These documents become the knowledge base.

---

## Step 4 — Embedding Generation

The documents are converted into vectors.

A vector is simply a numerical representation of meaning.

Instead of storing words,

we store mathematical representations of those words.

This allows two completely different sentences with similar meaning to be close together in vector space.

---

# Why Embeddings?

Traditional search compares:

```
Word == Word
```

Embeddings compare:

```
Meaning ≈ Meaning
```

That is why semantic search works.

---

# What is Chroma DB?

Chroma is a Vector Database.

Unlike SQL databases,

which store structured rows,

Chroma stores vectors.

Example:

```
Issue
↓

Embedding Model

↓

[0.24, -0.83, 0.11, ...]

↓

Stored in Chroma
```

Later,

when a new issue arrives,

its embedding is generated.

Instead of scanning every issue manually,

Chroma performs a nearest-neighbor search and returns the most similar vectors.

This makes semantic retrieval fast and scalable.

---

# Why Chroma?

We chose Chroma because:

- Lightweight
- Easy local setup
- LangChain integration
- No external server required
- Ideal for MVPs
- Excellent documentation

---

# Alternatives Considered

Other vector databases include:

- FAISS
- Pinecone
- Weaviate
- Qdrant
- Milvus

### Why not FAISS?

FAISS is excellent for similarity search,

but it is primarily a vector index.

Chroma provides a higher-level developer experience and integrates naturally with LangChain.

### Why not Pinecone?

Pinecone is cloud-based.

The goal of this MVP was to run locally without requiring external infrastructure.

### Why not Weaviate or Qdrant?

Both are excellent production databases,

but they require additional setup.

For rapid development,

Chroma provided the best balance between simplicity and functionality.

---

# Why LangChain Documents?

LangChain standardizes how text is represented.

It allows metadata and content to travel together through the pipeline.

This makes retrieval cleaner and easier to extend.

---

# Why Semantic Search Instead of Keyword Search?

Consider these two issues:

Issue A

> API crashes while validating aliases.

Issue B

> FastAPI throws exception during alias parsing.

Keyword search may fail.

Semantic search recognizes they describe the same underlying problem.

That is exactly what VibeForge aims to solve.

---

# Tech Stack

## Backend

- Python

## LLM

- Google Gemini

## Embeddings

- sentence-transformers/all-mpnet-base-v2

## Vector Database

- Chroma DB

## Frameworks

- LangChain

## Interface

- Gradio

## APIs

- GitHub REST API

---

# Complete Workflow

```
GitHub Repository

↓

GitHub API

↓

Raw JSON

↓

Processed Issues

↓

LangChain Documents

↓

Embedding Model

↓

Chroma Vector Database

↓

Repository Indexed

↓

User Query

↓

Issue Analysis (Gemini)

↓

Similarity Search (Chroma)

↓

Retrieved Issues

↓

Duplicate Detection (Gemini)

↓

Final Response
```

---

# Repository Structure

```
VibeForge/

├── data/
│   └── .gitkeep
│
├── src/
│   ├── github_client.py
│   ├── process_issues.py
│   ├── create_documents.py
│   ├── embeddings.py
│   ├── vector_db.py
│   ├── find_similar_issues.py
│   ├── llm_issue_analyzer.py
│   └── llm_duplicate_analyzer.py
│
├── main.py
├── pyproject.toml
└── README.md
```

---

# Installation

```bash
git clone <repository-url>

cd VibeForge

uv sync

uv run main.py
```

---

# Future Improvements

- Repository health insights
- Pull Request analysis
- Contributor intelligence
- Incremental indexing
- Local LLM support
- Private repository support
- Multi-repository search
- Automatic issue labeling
- Repository-wide RAG
- Interactive dashboard
- Performance optimizations

---

# License

This project is licensed under the MIT License.

---

## Built with ❤️ to Forge Better Repositories.