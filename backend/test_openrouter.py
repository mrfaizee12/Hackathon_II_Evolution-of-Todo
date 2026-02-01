#!/usr/bin/env python3
"""
Test script to verify OpenRouter API connectivity and functionality
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.openrouter_service import OpenRouterService
from src.database.config import settings


def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    print("Testing OpenRouter API connection...")

    # Check if API key is set
    if not settings.openrouter_api_key:
        print("[ERROR]: OPENROUTER_API_KEY is not set in the environment")
        return False

    print(f"[OK] API key is set (first 8 chars: {settings.openrouter_api_key[:8]}...)")

    try:
        # Initialize the service
        service = OpenRouterService()
        print("[OK] OpenRouter service initialized successfully")

        # Test a simple API call without tools
        messages = [
            {"role": "user", "content": "Hello, are you available?"}
        ]

        print("Sending test message to OpenRouter API...")
        response_result = service.chat_completion(messages=messages)

        if response_result["success"]:
            print("[OK] OpenRouter API call succeeded!")
            response = response_result["response"]
            if hasattr(response.choices[0].message, 'content'):
                content = response.choices[0].message.content
                print(f"[OK] Received response: {content[:100]}...")
            else:
                print("[WARN] Response received but no content in message")
        else:
            print(f"[ERROR] OpenRouter API call failed: {response_result.get('message', 'Unknown error')}")
            if 'error' in response_result:
                print(f"Error details: {response_result['error']}")
            return False

        return True

    except Exception as e:
        print(f"[ERROR] Error testing OpenRouter API: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False


def test_with_tools():
    """Test OpenRouter API with tools"""
    print("\nTesting OpenRouter API with tools...")

    try:
        service = OpenRouterService()

        # Define a simple tool
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Get the current time",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

        # Test message that should trigger tool use
        messages = [
            {"role": "user", "content": "What time is it?"}
        ]

        print("Sending tool test message to OpenRouter API...")
        response_result = service.chat_completion(messages=messages, tools=tools)

        if response_result["success"]:
            print("[OK] OpenRouter API call with tools succeeded!")
            response = response_result["response"]
            if hasattr(response.choices[0].message, 'tool_calls'):
                print(f"[OK] Tool calls detected: {bool(response.choices[0].message.tool_calls)}")
            if hasattr(response.choices[0].message, 'content'):
                content = response.choices[0].message.content
                print(f"Response content: {content[:100] if content else 'None'}...")
        else:
            print(f"[ERROR] OpenRouter API call with tools failed: {response_result.get('message', 'Unknown error')}")
            if 'error' in response_result:
                print(f"Error details: {response_result['error']}")
            return False

        return True

    except Exception as e:
        print(f"[ERROR] Error testing OpenRouter API with tools: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    print("OpenRouter API Connectivity Test")
    print("=" * 40)

    success1 = test_openrouter_connection()
    success2 = test_with_tools()

    print("\n" + "=" * 40)
    if success1 and success2:
        print("[SUCCESS] All tests passed! OpenRouter API is working correctly.")
    else:
        print("[FAILED] Some tests failed. Please check the OpenRouter API configuration.")

    print("=" * 40)