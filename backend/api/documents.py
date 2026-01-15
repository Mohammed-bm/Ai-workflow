import time
from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from services.vector_store_service import vector_store
from services.embedding_service import EmbeddingService
from utils.chunking import chunk_text

router = APIRouter(prefix="/documents", tags=["documents"])
embedding_service = EmbeddingService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload PDF and store in ChromaDB embeddings"""
    start = time.time()
    print(f"🟢 Upload started: {file.filename}")
    
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # 1. Read PDF bytes
        print("📄 Reading PDF...")
        pdf_bytes = await file.read()
        print(f"✅ Read {len(pdf_bytes)} bytes ({time.time() - start:.2f}s)")
        
        # 2. Extract text
        print("📝 Extracting text...")
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        extracted_text = ""

        for page in doc:
            extracted_text += page.get_text()

        doc.close()

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        print(f"✅ Extracted {len(extracted_text)} characters ({time.time() - start:.2f}s)")

        # 3. Chunk text
        print("✂️ Chunking text...")
        chunks = chunk_text(extracted_text, chunk_size=500, overlap=50)

        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to create text chunks")

        print(f"✅ Created {len(chunks)} chunks ({time.time() - start:.2f}s)")

        # 4. Generate embeddings
        print("🧠 Generating embeddings...")
        embeddings = embedding_service.embed_texts(chunks)
        print(f"✅ Generated {len(embeddings)} embeddings ({time.time() - start:.2f}s)")

        # 🧹 5. CLEAR VECTOR DB (IMPORTANT)
        vector_store.hard_reset()

        # 6. Prepare metadata
        metadatas = [
            {
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        # 7. Store in ChromaDB
        print("💾 Storing in ChromaDB...")
        vector_store.add_text(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        total_time = time.time() - start
        print(f"🎉 Upload complete in {total_time:.2f}s")

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "processing_time": f"{total_time:.2f}s",
            "message": "Document uploaded and indexed successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
