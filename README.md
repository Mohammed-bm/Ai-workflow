# 🔄 No-Code Workflow Builder

**An AI-powered no-code platform for building and executing intelligent workflows.**  
An AI-powered no-code platform for visually building, saving, loading, and executing intelligent workflows using a drag-and-drop canvas.

Users can design workflows by connecting components (User Query → Knowledge Base → LLM → Output), persist them in a database, and dynamically execute them using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Project Overview

This project demonstrates a full-stack AI system combining:
- Visual workflow orchestration (React Flow)
- Backend workflow persistence & execution (FastAPI)
- Document-aware AI responses (RAG)
- Vector search using embeddings
The focus is on system design, API clarity, and real-world AI pipelines, not just UI.
---

## 🎯 Key Features

- ✅ Visual Workflow Builder with drag-and-drop interface (React Flow)  
- ✅ Document Processing: Upload PDFs, extract text, generate embeddings  
- ✅ Vector Search: ChromaDB for semantic similarity and context retrieval  
- ✅ RAG Pipeline: Retrieval-Augmented Generation for accurate answers  
- ✅ Workflow Validation: Graph-based validation with error detection  
- ✅ Dynamic Execution: Orchestrates workflows based on user-defined connections  
- ✅ Free LLM Integration: Google Gemini for zero-cost AI responses  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repo  
```bash
git clone https://github.com/Mohammed-bm/Ai-wrokflow.git
```

### 2️⃣ Environment Variables  
Create `.env` file in `backend/` folder:  

#### Example: `backend/.env`  
```env
# Required: Google Gemini for LLM (FREE)
GOOGLE_API_KEY=AIza-your-google-gemini-key-here

# Optional: PostgreSQL (for production)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

**Get Free API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Google Gemini: https://aistudio.google.com/app/apikey

### 3️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**  
API Documentation: **http://localhost:8000/docs**

### 4️⃣ Frontend Setup (Coming Soon)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## 📚 Usage Flow

1. User creates workflow in visual canvas →  
2. Connects: User Query → Knowledge Base → LLM Engine → Output →  
3. Validates workflow structure →  
4. Uploads PDF documents to Knowledge Base →  
5. User sends question via chat interface →  
6. System retrieves relevant document chunks (Vector Search) →  
7. Combines query + context → LLM (Gemini) →  
8. Returns AI-generated answer with sources

---

## 🌐 Deployment

### Planned Deployment
- Backend → Render / Railway / AWS  
- Frontend → Vercel / Netlify  
- Database → Neon (Serverless PostgreSQL)  
- Vector Store → Pinecone / Weaviate (production)

---

## 📸 Sample Screenshots 

![Workflow Builder](images/workflowbuilder.png)  
- Screenshot: Visual workflow builder with drag-and-drop components

![Validation Results](images/validation.png)  
- Screenshot: Real-time workflow validation with error detection

![Execution Results](images/execution.png)  
- Screenshot: AI-generated responses with source citations

![Saved Workflows](images/savedworkflows.png)  
- Screenshot: Persistent workflow management with database-backed save and reload support

---

## 🏗️ Architecture Overview

This project uses a simple but powerful architecture designed for AI-powered workflow automation.  
Here's how it works:

1. **Frontend (React)** provides a visual canvas for building workflows using React Flow.  
2. **FastAPI Backend** exposes 4 core REST APIs for document upload, workflow validation, execution, and chat.  
3. **Document Processing** extracts text from PDFs using PyMuPDF, chunks it, and generates embeddings via OpenAI.  
4. **ChromaDB** stores document embeddings as vectors and performs semantic similarity search.  
5. **Workflow Executor** orchestrates component execution based on user-defined graph structure.  
6. **Google Gemini LLM** generates context-aware responses combining user queries with retrieved document chunks.  
7. **Chat Interface** displays responses with source attribution and maintains conversation history.

### 📊 Architecture Diagram

![Architecure Diagram](images/architecture.png)  

---

## 📜 License

MIT License © 2025

---

## ✅ Note

This project is built as a **Full-Stack Engineering Assignment** demonstrating:  
- Backend API design (FastAPI)  
- AI/ML integration (RAG, embeddings, LLMs)  
- Vector databases & semantic search  
- Workflow orchestration & graph processing  
- Clean architecture & modular design  

---

## 👤 Author

**Mohammed Ahmed Awadh Bin Mahfoudh**  
- GitHub: [@Mohammed-bm](https://github.com/Mohammed-bm)  
- LinkedIn: [Mohammed Bin Mahfoudh](https://linkedin.com/in/mohammed-bin-mahfoudh)

---

## 🙏 Acknowledgments

- FastAPI for the web framework  
- ChromaDB for vector storage  
- Google Gemini for free LLM access  
- OpenAI for embeddings API  
- React Flow for workflow visualization  
- The open-source community
