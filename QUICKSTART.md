# 🚀 How to Run SHL Assessment Recommender

## Quick Start (3 Steps)

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Setup & Build Index**
```bash
# Build the embedding index (one-time)
python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl
```

### **Step 3: Start the API Server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Server will start at: **http://localhost:8000**

---

## Test the API (While Server is Running)

### In another terminal, test with curl:

#### **Health Check**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

---

#### **Test 1: Ask Vague Question (Bot Clarifies)**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I need an assessment"}]}'
```

Expected: Bot asks clarification (no recommendations yet)

---

#### **Test 2: Recommend Java Developer**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hiring a Java developer"}]}'
```

Expected: 1-10 Java-related assessments with URLs

---

#### **Test 3: Multi-turn Conversation**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role":"user","content":"I need to hire someone"},
      {"role":"assistant","content":"What role are you hiring for?"},
      {"role":"user","content":"QA tester with automation skills"}
    ]
  }'
```

Expected: Recommendations for QA assessments

---

#### **Test 4: Compare Assessments**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Difference between Java and Python?"}]}'
```

Expected: Bot explains both assessments

---

#### **Test 5: Off-topic Question (Should Refuse)**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is the weather?"}]}'
```

Expected: Bot refuses to answer

---

## Automated Test Suite

Run all tests at once:

```bash
python test_chat.py
```

This will:
- Run 8 comprehensive test cases
- Check all required response fields
- Report pass/fail status
- Show recommendations returned

---

## API Documentation

Once server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Full Automated Setup Script

Or run everything in one command:

```bash
python run_project.py
```

This will:
1. ✅ Install dependencies
2. ✅ Install Playwright browsers
3. ✅ Scrape SHL catalog
4. ✅ Build embedding index
5. ✅ Start the API server

---

## Project Structure

```
d:\SHL\
├── app/
│   ├── main.py                 # FastAPI app with /health and /chat
│   ├── core/config.py          # Settings
│   └── services/
│       ├── catalog.py          # Assessment dataclass
│       ├── recommender.py      # Intent extraction + recommendations
│       └── retrieval.py        # Embedding search
├── scripts/
│   ├── scrape_catalog.py       # Scrape SHL (39 assessments)
│   └── build_index.py          # Build embedding index
├── data/
│   ├── catalog.json            # 39 SHL assessments
│   └── index.pkl               # Binary embedding index
├── requirements.txt            # Python dependencies
├── test_chat.py               # Test suite
├── run_project.py             # One-command setup script
└── README.md                  # This file
```

---

## Troubleshooting

### **Server won't start**
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# If in use, kill it:
taskkill /PID <PID> /F
```

### **Tests fail with connection error**
- Make sure API server is running in another terminal
- Check http://localhost:8000/health returns `{"status": "ok"}`

### **Slow embedding index build**
- First time: 30-60 seconds (downloads model)
- Subsequent: 5-10 seconds (cached model)

### **No recommendations returned**
- Check that `data/catalog.json` exists (39 assessments)
- Check that `data/index.pkl` exists
- Verify query contains role or skill keywords

---

## Key Features Implemented

✅ **Conversational**: Multi-turn conversations with full history  
✅ **Semantic Search**: Local embeddings via SentenceTransformers  
✅ **Zero API Keys**: No Gemini/OpenAI required  
✅ **Rule-Based Intent**: Deterministic (no hallucinations)  
✅ **Guardrails**: Rejects off-topic and prompt injection  
✅ **SHL Catalog**: 39 individual assessments (no job solutions)  
✅ **Stateless**: Full conversation history in each request  
✅ **Fast**: <1s response time per query  

---

## Next Steps

1. Run `python run_project.py` to setup everything
2. Run `python test_chat.py` to test all endpoints
3. Try manual curl requests to understand the API
4. Visit http://localhost:8000/docs for full API docs

Happy testing! 🎉
