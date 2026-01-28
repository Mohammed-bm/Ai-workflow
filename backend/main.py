from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from api import documents, workflows, execute

app = FastAPI(title="AI Workflow Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (only once each!)
app.include_router(documents.router)
app.include_router(workflows.router)
app.include_router(execute.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI Workflow Backend running"}
