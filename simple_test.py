#!/usr/bin/env python3
"""
Simple test for the TDS Virtual TA API.
"""

import requests
import json

def main():
    print("=== TDS Virtual TA API Tests ===")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✓ Health Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return
    
    # Test question endpoint
    print("\n2. Testing question endpoint...")
    test_questions = [
        "What model should I use for GA5 question 8?",
        "How does GA4 scoring work?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n2.{i} Testing: '{question}'")
        try:
            payload = {"question": question}
            response = requests.post(
                "http://localhost:8000/api/ask",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            print(f"✓ Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Answer: {result.get('answer', 'No answer')[:100]}...")
                links = result.get('links', [])
                print(f"✓ Links found: {len(links)}")
                for link in links[:2]:  # Show first 2 links
                    print(f"  - {link.get('text', 'No title')}: {link.get('url', 'No URL')}")
            else:
                print(f"✗ Error response: {response.text}")
        except Exception as e:
            print(f"✗ Question endpoint error: {e}")
    
    print("\n=== Tests Completed ===")

if __name__ == "__main__":
    main()
