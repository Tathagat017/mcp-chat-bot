#!/usr/bin/env python3
"""
Simple test script to verify the MCP Q&A API is working
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_ask_question():
    """Test ask endpoint"""
    print("\n🤖 Testing ask endpoint...")
    
    test_questions = [
        "What is Model Context Protocol?",
        "How does MCP work?",
        "What are the benefits of using MCP?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        
        try:
            payload = {
                "question": question,
                "include_sources": True,
                "top_k": 3
            }
            
            response = requests.post(
                f"{API_BASE_URL}/ask",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Answer received (took {result.get('processing_time', 0):.2f}s)")
                print(f"   Answer: {result['answer'][:100]}...")
                if result.get('sources'):
                    print(f"   Sources: {len(result['sources'])} found")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def test_root():
    """Test root endpoint"""
    print("\n🏠 Testing root endpoint...")
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Message: {response.json()['message']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MCP Q&A API Test Suite")
    print("=" * 30)
    
    # Test if server is running
    print("🚀 Checking if server is running...")
    try:
        response = requests.get(API_BASE_URL, timeout=5)
        print("✅ Server is running")
    except requests.exceptions.RequestException:
        print("❌ Server is not running!")
        print("💡 Start the server with: python run_server.py")
        return
    
    # Run tests
    test_root()
    test_health()
    test_ask_question()
    
    print("\n🎉 Test suite completed!")
    print("📚 Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main() 