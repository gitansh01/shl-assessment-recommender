# 📝 COMPLETE WORKING CODE - Copy & Paste to Run

## For Windows Users: Simplest Method

### **Step 1: Open Command Prompt in `d:\SHL`**

```cmd
cd d:\SHL
```

### **Step 2: Run single command**

```cmd
run.bat
```

Done! ✅ Server will start automatically.

---

## For Any Platform: Python Method

### **Step 1: Open terminal in `d:\SHL`**

```bash
cd d:\SHL
```

### **Step 2: Run single command**

```bash
python run_project.py
```

Done! ✅ Server will start automatically.

---

## For Full Control: Manual Steps

### **Terminal 1: Setup & Start Server**

```bash
# 1. Install dependencies (first time only)
pip install -r requirements.txt

# 2. Build embedding index (first time only)
python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl

# 3. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

### **Terminal 2: Run Tests**

```bash
# Run automated test suite
python test_chat.py
```

**Expected output:**
```
==============================================================================
  🧪 SHL Assessment Recommender - Test Suite
==============================================================================

⏳ Checking server connectivity...
✅ Server is running: 200

...

📊 Test Summary
═══════════════════════════════════════════════════════════════════════════

✅ Passed: 8
❌ Failed: 0
📈 Total: 8
🎯 Success Rate: 100.0%

🎉 All tests passed!
```

---

## 🧪 Testing Code to Copy-Paste

### **Test 1: Health Check (Works Immediately)**

```bash
curl http://localhost:8000/health
```

### **Test 2: Clarify Intent**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I need an assessment"}]}'
```

### **Test 3: Get Recommendations**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hiring a Java developer"}]}'
```

### **Test 4: Multi-turn Conversation**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role":"user","content":"I need to hire"},
      {"role":"assistant","content":"What role?"},
      {"role":"user","content":"Java developer"}
    ]
  }'
```

### **Test 5: Compare Assessments**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Difference between OPQ and GSA?"}]}'
```

### **Test 6: Off-topic Refusal**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is 2+2?"}]}'
```

---

## 📤 Sample API Responses

### **Response 1: Clarification (Vague Input)**

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "I need an assessment"}
  ]
}
```

**Response:**
```json
{
  "reply": "I'd like to help you find the right assessment! Could you tell me what role you're hiring for? For example, are you looking to assess a Java developer, QA engineer, product manager, etc.?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

### **Response 2: Recommendation (Clear Input)**

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hiring a senior Java developer with strong communication"}
  ]
}
```

**Response:**
```json
{
  "reply": "Great! I found relevant assessments for Java developers focusing on technical and communication skills. Here are 5 SHL assessments that would be perfect for your hiring needs:",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "K",
      "description": "Assesses knowledge of Java 8 syntax and OOP concepts"
    },
    {
      "name": "DACT - Digital",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "P",
      "description": "Personality assessment measuring communication and leadership"
    },
    {
      "name": "Verify G+",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "A",
      "description": "Numerical reasoning for technical roles"
    },
    {
      "name": "Verify V+",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "A",
      "description": "Verbal reasoning"
    },
    {
      "name": "Verify I+",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "A",
      "description": "Inductive reasoning"
    }
  ],
  "end_of_conversation": false
}
```

---

### **Response 3: Multi-turn Refinement**

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "I need to hire"},
    {"role": "assistant", "content": "What role are you hiring for?"},
    {"role": "user", "content": "QA tester with automation skills"}
  ]
}
```

**Response:**
```json
{
  "reply": "Perfect! For QA testers with automation skills, I recommend these technical and aptitude assessments to evaluate both manual and automated testing capabilities:",
  "recommendations": [
    {
      "name": "QA Tester - JAVA",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "K",
      "description": "Tests Java knowledge for QA automation"
    },
    {
      "name": "Verify G+",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "A",
      "description": "Logical reasoning for test case creation"
    },
    {
      "name": "DACT - Digital",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "P",
      "description": "Assess collaboration and communication skills"
    }
  ],
  "end_of_conversation": false
}
```

---

### **Response 4: Comparison**

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Difference between OPQ and GSA?"}
  ]
}
```

**Response:**
```json
{
  "reply": "Both OPQ and GSA are personality assessments from SHL, but they measure different aspects:\n\n**OPQ (Occupational Personality Questionnaire)**:\n- Measures 32 personality factors\n- More detailed and comprehensive\n- Best for senior roles and cultural fit\n\n**GSA (General Skils Assessment)**:\n- Personality and ability combined\n- Quicker assessment\n- Good for entry-level roles",
  "recommendations": [
    {
      "name": "OPQ",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "P"
    },
    {
      "name": "GSA",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "A"
    }
  ],
  "end_of_conversation": false
}
```

---

### **Response 5: Off-topic Refusal**

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "What is the capital of France?"}
  ]
}
```

**Response:**
```json
{
  "reply": "I can only help with questions related to SHL assessments and hiring. I don't have information about general topics like geography. Can I help you find the right assessment for a role you're trying to fill?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## 📊 Test Output Example

When you run `python test_chat.py`, you'll see:

```
══════════════════════════════════════════════════════════════════════════
  🧪 SHL Assessment Recommender - Test Suite
══════════════════════════════════════════════════════════════════════════

⏳ Checking server connectivity...
✅ Server is running: 200

▶ Test: Health Check
📍 URL: http://localhost:8000/health
📌 Method: GET
✅ Status Code: 200

📤 Response:
  status: ok
✅ Test PASSED

▶ Test: Clarify - Vague Request
📍 URL: http://localhost:8000/chat
📌 Method: POST
✅ Status Code: 200

📤 Response:
  reply: I'd like to help you find...
  recommendations: []
  end_of_conversation: false
✅ Test PASSED

... (6 more tests)

══════════════════════════════════════════════════════════════════════════
📊 Test Summary
══════════════════════════════════════════════════════════════════════════

✅ Passed: 8
❌ Failed: 0
📈 Total: 8
🎯 Success Rate: 100.0%

🎉 All tests passed!
```

---

## ✅ Verification Checklist

After running `python run_project.py` or `run.bat`:

- [ ] Dependencies installed (`pip list | grep sentence`)
- [ ] `data/catalog.json` exists (39 assessments)
- [ ] `data/index.pkl` created (embeddings)
- [ ] Server running at `http://localhost:8000`
- [ ] `curl http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] `python test_chat.py` shows 8/8 tests passed

If all checkmarks passed: ✅ **Project is working!**

---

## 🔗 URLs to Access

- **API Health**: http://localhost:8000/health
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Chat Endpoint**: POST to http://localhost:8000/chat

---

## 💾 Output Files Generated

After first run, these are created:

```
data/
├── catalog.json          ← 39 SHL assessments (scraped)
├── index.pkl             ← Embeddings index (~8MB, binary)
└── [cache/]              ← Sentence-transformers model cache
```

---

## ⏱️ Timing Guide

| Operation | Time | Notes |
|-----------|------|-------|
| `pip install` | 30-60s | First time only |
| `playwright install` | 1-2 min | First time only, ~200MB |
| `build_index.py` (first) | 30-60s | Downloads model, generates embeddings |
| `build_index.py` (cached) | 5-10s | Model already cached |
| Server startup | 2-3s | Loads embeddings index |
| Single API request | 0.1-0.5s | Query → search → response |

---

## 🎯 You're Done!

Your SHL Assessment Recommender is now:
- ✅ Running
- ✅ Tested
- ✅ Ready to use

**Next steps:**
1. Explore `/docs` for interactive API testing
2. Modify intent rules in `app/services/recommender.py`
3. Customize response messages
4. Deploy to Render/Railway (see DEPLOYMENT.md)

Happy coding! 🚀
