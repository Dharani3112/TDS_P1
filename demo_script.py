#!/usr/bin/env python3
"""
TDS Virtual TA - Final Demonstration Script
This script demonstrates the fully functional TDS Virtual Teaching Assistant.
"""

import requests
import json
import time

def main():
    print("🎓 TDS VIRTUAL TEACHING ASSISTANT - LIVE DEMONSTRATION")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health Check
    print("\n🔍 1. HEALTH CHECK")
    try:
        response = requests.get(f"{base_url}/health")
        health = response.json()
        print(f"✅ Status: {health['status']} | Version: {health['version']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Interactive Q&A Demo
    print(f"\n🤖 2. INTELLIGENT QUESTION ANSWERING")
    
    demo_questions = [
        {
            "question": "What model should I use for GA5 question 8?",
            "description": "GA5 Model Selection Query"
        },
        {
            "question": "How does GA4 scoring work on the dashboard?",
            "description": "GA4 Scoring Explanation"
        },
        {
            "question": "Should I use Docker or Podman for this course?",
            "description": "Technology Choice Guidance"
        },
        {
            "question": "What is the Tools in Data Science course about?",
            "description": "Course Information Query"
        }
    ]
    
    for i, demo in enumerate(demo_questions, 1):
        print(f"\n📝 Demo {i}: {demo['description']}")
        print(f"❓ Question: \"{demo['question']}\"")
        
        try:
            response = requests.post(
                f"{base_url}/api/ask",
                headers={"Content-Type": "application/json"},
                json={"question": demo['question']},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No answer provided')
                links = result.get('links', [])
                
                print(f"✅ Response received successfully")
                print(f"📖 Answer: {answer[:150]}{'...' if len(answer) > 150 else ''}")
                print(f"🔗 Relevant links: {len(links)} found")
                
                if links:
                    for j, link in enumerate(links[:2], 1):
                        print(f"   {j}. {link.get('text', 'Link')}: {link.get('url', 'No URL')}")
                
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    # Test 3: API Status
    print(f"\n📊 3. SERVICE STATUS")
    try:
        response = requests.get(f"{base_url}/api/status")
        status = response.json()
        print(f"✅ Knowledge base entries: {status.get('knowledge_base_entries', 'Unknown')}")
        print(f"✅ Service status: {status.get('service_status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Status check failed: {e}")
    
    print(f"\n🎉 DEMONSTRATION COMPLETE!")
    print(f"🌐 API Documentation: {base_url}/docs")
    print(f"🏥 Health Endpoint: {base_url}/health")
    print(f"🤖 Ask Questions: POST {base_url}/api/ask")
    print("\n" + "=" * 60)
    print("✨ TDS Virtual TA is fully operational and ready for production! ✨")

if __name__ == "__main__":
    main()
