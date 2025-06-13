#!/usr/bin/env python3
"""
Interactive Testing Tool for TDS Virtual TA
This script allows you to test questions interactively and see detailed responses.
"""

import requests
import json
import sys

def interactive_test():
    """Interactive testing mode where you can type questions."""
    print("🎓 TDS VIRTUAL TA - INTERACTIVE TESTING MODE")
    print("=" * 50)
    print("Type your questions and see how the Virtual TA responds!")
    print("Commands:")
    print("  - Type any question to test it")
    print("  - Type 'quit' or 'exit' to stop")
    print("  - Type 'help' to see sample questions")
    print("  - Type 'status' to check system status")
    print("-" * 50)
    
    base_url = "http://localhost:8000"
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ TDS Virtual TA is online and ready!")
        else:
            print("❌ Server is not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the server is running with: uvicorn app.main:app --reload --port 8000")
        return
    
    question_count = 0
    
    while True:
        try:
            print(f"\n💬 Question #{question_count + 1}:")
            user_input = input("❓ Ask me anything about TDS: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for testing the TDS Virtual TA!")
                break
                
            elif user_input.lower() == 'help':
                show_sample_questions()
                continue
                
            elif user_input.lower() == 'status':
                check_system_status(base_url)
                continue
            
            # Process the question
            question_count += 1
            print(f"\n🤖 Processing your question...")
            
            try:
                response = requests.post(
                    f"{base_url}/api/ask",
                    headers={"Content-Type": "application/json"},
                    json={"question": user_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('answer', 'No answer provided')
                    links = result.get('links', [])
                    
                    print(f"✅ Response received!")
                    print(f"\n📖 Answer:")
                    print("-" * 40)
                    print(answer)
                    print("-" * 40)
                    
                    if links:
                        print(f"\n🔗 Relevant links ({len(links)} found):")
                        for i, link in enumerate(links, 1):
                            print(f"{i}. {link.get('text', 'Link')}")
                            print(f"   URL: {link.get('url', 'No URL')}")
                    else:
                        print("\n🔗 No relevant links found")
                        
                else:
                    print(f"❌ Error: HTTP {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error processing question: {e}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def show_sample_questions():
    """Show sample questions that work well."""
    print("\n📝 SAMPLE QUESTIONS TO TRY:")
    print("-" * 30)
    
    samples = [
        "What model should I use for GA5 question 8?",
        "How does GA4 scoring work on the dashboard?",
        "Should I use Docker or Podman for this course?",
        "What is the Tools in Data Science course about?",
        "How are assignments graded in TDS?",
        "What programming languages are used in TDS?",
        "When is the submission deadline for GA4?",
        "Can you help me understand the course structure?",
        "What tools do I need for this course?",
        "How do I submit my assignments?"
    ]
    
    for i, question in enumerate(samples, 1):
        print(f"{i:2d}. {question}")

def check_system_status(base_url):
    """Check the system status and display information."""
    print("\n🔍 SYSTEM STATUS CHECK")
    print("-" * 25)
    
    try:
        # Health check
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health: {health_data.get('status', 'Unknown')}")
            print(f"📦 Version: {health_data.get('version', 'Unknown')}")
        else:
            print("❌ Health check failed")
            
        # Status check
        status_response = requests.get(f"{base_url}/api/status", timeout=5)
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"📊 Service Status: {status_data.get('status', 'Unknown')}")
            print(f"📚 Knowledge Base Entries: {status_data.get('knowledge_base_entries', 'Unknown')}")
        else:
            print("❌ Status check failed")
            
    except Exception as e:
        print(f"❌ Cannot check status: {e}")

def batch_test_from_file(filename):
    """Test questions from a file (one question per line)."""
    print(f"📁 BATCH TESTING FROM: {filename}")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
            
        if not questions:
            print("❌ No questions found in file")
            return
            
        print(f"Found {len(questions)} questions to test\n")
        
        passed = 0
        for i, question in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] Testing: {question[:50]}...")
            
            try:
                response = requests.post(
                    f"{base_url}/api/ask",
                    headers={"Content-Type": "application/json"},
                    json={"question": question},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get('answer', '')
                    if len(answer) > 10:
                        print(f"✅ Got answer ({len(answer)} chars)")
                        passed += 1
                    else:
                        print("⚠️  Short or empty answer")
                else:
                    print(f"❌ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
        print(f"\n📊 Batch Test Results: {passed}/{len(questions)} passed")
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch" and len(sys.argv) > 2:
            batch_test_from_file(sys.argv[2])
        else:
            print("Usage:")
            print("  python interactive_test.py              # Interactive mode")
            print("  python interactive_test.py --batch <file>  # Batch test from file")
    else:
        interactive_test()
