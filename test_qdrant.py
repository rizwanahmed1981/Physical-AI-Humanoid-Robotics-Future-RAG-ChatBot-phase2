#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot/Physical-AI-Humanoid-Robotics-Future-phase-2/backend/.env')

# Add the backend directory to the Python path to resolve imports
sys.path.insert(0, '/home/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot/Physical-AI-Humanoid-Robotics-Future-phase-2/backend')

try:
    from app.services.qdrant_service import QdrantService
    print("QdrantService imported successfully")

    # Try to create Qdrant service
    qdrant_service = QdrantService()
    print("QdrantService initialized successfully")

    # Try to create collection
    import asyncio
    async def test():
        await qdrant_service.create_collection(vector_size=1024)
        print("Qdrant collection created successfully")

    asyncio.run(test())
    print("Qdrant test completed successfully")

except Exception as e:
    print(f"Error with Qdrant: {e}")
    import traceback
    traceback.print_exc()