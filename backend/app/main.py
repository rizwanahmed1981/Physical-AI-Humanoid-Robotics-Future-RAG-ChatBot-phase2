from fastapi import FastAPI
from app.api.health import health_router
from app.api.rag import rag_router

app = FastAPI(title="Physical AI RAG Backend")

# Include health router
app.include_router(health_router, prefix="/health", tags=["Health"])

# Include RAG router
app.include_router(rag_router)

@app.get("/")
async def root():
    return {"message": "Physical AI RAG Backend is running"}