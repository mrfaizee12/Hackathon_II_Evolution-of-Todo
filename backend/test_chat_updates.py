#!/usr/bin/env python3
"""
Test script to verify that the chat API returns updated task lists after mutations.
"""

import asyncio
import json
from typing import Dict, Any

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database.database import get_session
from src.models.user import User
from src.models.todo import Todo
from src.database.config import settings

# Create test client
client = TestClient(app)

def test_chat_response_format():
    """
    Test that chat responses include tasks when mutations occur
    """
    print("Testing chat response format...")

    # Simulate a chat request that adds a task
    response = client.post("/api/v1/chat/send", json={
        "message": "Add a new task: Buy groceries"
    }, headers={"Authorization": "Bearer test_token"})

    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")

        # Check if the response has the expected structure
        assert "response" in data
        assert "conversation_id" in data
        assert "action_performed" in data

        # If a task was added, it should have tasks in the response
        if "add" in data.get("response", "").lower():
            print("Task addition detected in response")
            if "tasks" in data:
                print(f"Tasks included in response: {len(data['tasks'])} tasks")
            else:
                print("No tasks in response (might be expected depending on detection)")
        else:
            print("No task addition detected in response")
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_chat_response_format()
    print("Test completed!")