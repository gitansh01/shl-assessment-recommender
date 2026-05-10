#!/usr/bin/env python
"""Test suite for SHL Assessment Recommender chatbot."""

import json
import sys
import time
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000"
TIMEOUT = 10

test_cases = [
    {
        "name": "Health Check",
        "endpoint": "/health",
        "method": "GET",
        "expected_keys": ["status"],
    },
    {
        "name": "Clarify - Vague Request",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "I need an assessment"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Recommend - Java Developer",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "Hiring a Java developer with strong communication skills"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Recommend - Python Senior Dev",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "Need to assess a senior Python developer"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Conversation - Multi-turn",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "I need to hire"},
                {"role": "assistant", "content": "What role are you hiring for?"},
                {"role": "user", "content": "QA tester with automation skills"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Personality Assessment",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "Hiring for HR role, need personality assessment"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Compare Assessments",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "What is the difference between Java and C++?"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
    {
        "name": "Off-topic - Should Refuse",
        "endpoint": "/chat",
        "method": "POST",
        "data": {
            "messages": [
                {"role": "user", "content": "What is the weather today?"}
            ]
        },
        "expected_keys": ["reply", "recommendations", "end_of_conversation"],
    },
]


def print_header(text: str, char: str = "="):
    """Print a formatted header."""
    width = 70
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}")


def test_endpoint(test):
    """Test a single endpoint."""
    print_header(f"Test: {test['name']}", "▶")
    
    url = f"{BASE_URL}{test['endpoint']}"
    method = test["method"]
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        else:
            response = requests.post(
                url,
                json=test.get("data"),
                headers={"Content-Type": "application/json"},
                timeout=TIMEOUT
            )
        
        print(f"📍 URL: {url}")
        print(f"📌 Method: {method}")
        print(f"✅ Status Code: {response.status_code}")
        
        # Check status
        if response.status_code not in [200, 201]:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        
        # Check required keys
        missing_keys = [k for k in test["expected_keys"] if k not in data]
        if missing_keys:
            print(f"❌ Missing keys: {missing_keys}")
            return False
        
        # Pretty print response
        print(f"\n📤 Response:")
        print(f"  reply: {data.get('reply', 'N/A')[:100]}...")
        
        if data.get("recommendations"):
            print(f"  recommendations: {len(data['recommendations'])} assessments")
            for rec in data["recommendations"][:2]:
                print(f"    - {rec.get('name', 'Unknown')}")
            if len(data["recommendations"]) > 2:
                print(f"    ... and {len(data['recommendations']) - 2} more")
        else:
            print(f"  recommendations: []")
        
        print(f"  end_of_conversation: {data.get('end_of_conversation')}")
        
        print(f"✅ Test PASSED")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {url}")
        print(f"   Make sure the server is running on port 8000")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out (>{TIMEOUT}s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print_header("🧪 SHL Assessment Recommender - Test Suite", "═")
    
    # Check server connectivity
    print("\n⏳ Checking server connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {BASE_URL}")
        print(f"   Please start the server first:")
        print(f"   python run_project.py")
        sys.exit(1)
    
    # Run tests
    passed = 0
    failed = 0
    
    for test in test_cases:
        if test_endpoint(test):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print_header("📊 Test Summary", "═")
    print(f"\n✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {len(test_cases)}")
    print(f"🎯 Success Rate: {(passed/len(test_cases)*100):.1f}%\n")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
