import time
from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz
from services.vector_store_service import vector_store

from services.embedding_service import EmbeddingService
from utils.chunking import chunk_text

router = APIRouter(prefix="/documents", tags=["documents"])

embedding_service = EmbeddingService()

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    start = time.time()
    print("🟢 0. Request received")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    try:
        print("🟡 1. Reading PDF bytes")
        pdf_bytes = file.file.read()
        print(f"✅ PDF read: {len(pdf_bytes)} bytes ({time.time() - start:.2f}s)")

        print("🟡 2. Opening PDF with PyMuPDF")
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        print("🟡 3. Extracting text")
        extracted_text = ""
        for i, page in enumerate(doc):
            extracted_text += page.get_text()
        print(f"✅ Text extracted: {len(extracted_text)} chars ({time.time() - start:.2f}s)")

        print("🟡 4. Chunking text")
        chunks = chunk_text(extracted_text)
        print(f"✅ Chunks created: {len(chunks)} ({time.time() - start:.2f}s)")

        print("🟡 6. Generating embeddings")
        embeddings = embedding_service.embed_texts(chunks)
        print(f"✅ Embeddings done ({time.time() - start:.2f}s)")

        print("🟡 7. Preparing metadata")
        metadatas = [
            {"filename": file.filename, "chunk_index": i}
            for i in range(len(chunks))
        ]

        print("🔍 DEBUG")
        print("Chunks count:", len(chunks))
        print("Embeddings count:", len(embeddings))
        print("Metadatas count:", len(metadatas))

        print("🟡 8. Storing in ChromaDB")
        vector_store.add_text(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        print(f"✅ Stored in ChromaDB ({time.time() - start:.2f}s)")

        print("🟢 9. Returning response")
        return {
            "filename": file.filename,
            "chunks": len(chunks),
            "status": "stored"
        }

    except Exception as e:
        print("🔴 ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
