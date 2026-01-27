import time
from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz

from services.vector_store_service import get_vector_store
from services.embedding_service import get_embedding_model
from utils.chunking import chunk_text

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    start = time.time()
    print(f"🟢 Upload started: {file.filename}")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # 1️⃣ Read PDF
        pdf_bytes = await file.read()
        print(f"📄 Read {len(pdf_bytes)} bytes")

        # 2️⃣ Extract text
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        extracted_text = "".join(page.get_text() for page in doc)
        doc.close()

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # 3️⃣ Chunk text
        chunks = chunk_text(extracted_text, chunk_size=500, overlap=50)
        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to create chunks")

        # 4️⃣ Lazy-load embedding model
        embedding_model = get_embedding_model()
        embeddings = embedding_model.encode(
            chunks,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

        # 5️⃣ Lazy-load vector store
        vector_store = get_vector_store()

        print("🧹 Clearing ChromaDB collection")
        vector_store.clear_collection()

        # 6️⃣ Metadata
        metadatas = [
            {
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
            }
            for i in range(len(chunks))
        ]

        # 7️⃣ Store embeddings
        print("💾 Storing in ChromaDB...")
        vector_store.add_text(
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"🎉 Upload complete in {time.time() - start:.2f}s")

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks),
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
