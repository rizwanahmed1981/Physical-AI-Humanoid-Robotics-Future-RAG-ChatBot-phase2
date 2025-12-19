#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot/Physical-AI-Humanoid-Robotics-Future-phase-2/backend/.env')

# Add the backend directory to the Python path to resolve imports
sys.path.insert(0, '/home/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot/Physical-AI-Humanoid-Robotics-Future-phase-2/backend')

import cohere

# Test what the Cohere API returns
api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(api_key)

# Test with a simple text
test_texts = ["Hello world", "Test embedding"]
try:
    response = client.embed(
        texts=test_texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    print(f"Response type: {type(response)}")
    print(f"Embeddings type: {type(response.embeddings)}")
    print(f"First embedding type: {type(response.embeddings[0])}")
    print(f"First embedding: {response.embeddings[0][:5]}...")  # Show first 5 values

    # Try to access tolist method
    try:
        first_as_list = response.embeddings[0].tolist()
        print(f"tolist() method works: {type(first_as_list)}")
    except AttributeError:
        print("tolist() method does not exist, it's already a list or different type")
        print(f"Value itself: {response.embeddings[0][:5]}...")

except Exception as e:
    print(f"Error in test: {e}")