#!/usr/bin/env python3
"""
Test script for the TDS Virtual TA API.
"""

import requests
import json
import sys

def test_health_endpoint():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_question_endpoint(question):
    """Test the question endpoint."""
    print(f"\nTesting question: {question}")
    try:
        payload = {"question": question}
        response = requests.post(
            "http://localhost:8000/api/ask",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Answer: {result.get('answer', 'No answer')}")
        print(f"Links: {result.get('links', [])}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing question endpoint: {e}")
        return False

def main():
    """Main test function."""
    print("=== TDS Virtual TA API Tests ===\n")
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("Health endpoint failed. Server may not be running.")
        sys.exit(1)
    
    # Test questions
    test_questions = [
        "What model should I use for GA5 question 8?",
        "How does GA4 scoring work?",
        "What is Tools in Data Science about?",
        "Tell me about the course content",
    ]
    
    for question in test_questions:
        test_question_endpoint(question)
    
    print("\n=== Tests Completed ===")

if __name__ == "__main__":
    main()
