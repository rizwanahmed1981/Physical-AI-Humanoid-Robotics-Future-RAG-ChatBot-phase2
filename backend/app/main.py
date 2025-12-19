from fastapi import FastAPI
from app.api.health import health_router

app = FastAPI(title="Physical AI RAG Backend")

# Include health router
app.include_router(health_router, prefix="/health", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "Physical AI RAG Backend is running"}