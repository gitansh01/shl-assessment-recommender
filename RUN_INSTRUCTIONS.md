# 📋 COMPLETE GUIDE: Run & Test SHL Assessment Recommender

## ✅ Prerequisites

- **Python 3.9+** installed and in PATH
- **Windows**: Use Command Prompt or PowerShell
- **Port 8000** available (not in use)

---

## 🚀 Method 1: Automated Setup (Easiest - Windows)

### Run everything in one click:

```bash
run.bat
```

This will:
1. ✅ Install all dependencies
2. ✅ Install Playwright browsers
3. ✅ Build embedding index
4. ✅ Start API server

---

## 🚀 Method 2: Automated Setup (Python)

### Works on Windows/Mac/Linux:

```bash
python run_project.py
```

Same as Method 1 but cross-platform.

---

## 🚀 Method 3: Manual Step-by-Step (Full Control)

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

**What this installs:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sentence-transformers` - Local embeddings (free, no API key)
- `playwright` - Web scraping
- `joblib` - Save/load embeddings
- `requests` - HTTP client

---

### **Step 2: Setup Playwright** (One-time)
```bash
python -m playwright install
```

**Note:** This downloads browser engines (~200MB). Only needed once.

---

### **Step 3: Build Embedding Index** (One-time)
```bash
python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl
```

**Output:**
- Loads `data/catalog.json` (39 SHL assessments)
- Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Saves `data/index.pkl` (~8MB binary file)
- Time: First run ~30-60s, cached runs ~5-10s

---

### **Step 4: Start the API Server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Output should show:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **Server is now running!**

---

## 🧪 Testing the API

### **Open a NEW terminal/command prompt** and run tests:

### **Option A: Automated Test Suite** (Recommended)
```bash
python test_chat.py
```

This runs 8 comprehensive tests and shows results:
- ✅/❌ for each test
- Response preview
- Pass rate

---

### **Option B: Manual curl Tests**

#### **Test 1: Health Check**
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{"status": "ok"}
```

---

#### **Test 2: Vague Request → Bot Clarifies**
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"I need an assessment\"}]}"
```

**Expected:** Bot asks "What role?" → recommendations empty

---

#### **Test 3: Recommend - Java Developer**
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hiring a Java developer\"}]}"
```

**Expected:** Java assessments with SHL URLs

---

#### **Test 4: Multi-turn Conversation**
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hiring for QA\"},{\"role\":\"assistant\",\"content\":\"What skills?\"},{\"role\":\"user\",\"content\":\"Automation testing\"}]}"
```

**Expected:** QA + automation assessments

---

#### **Test 5: Compare Assessments**
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Compare Java and Python\"}]}"
```

**Expected:** Explanation of both assessments

---

#### **Test 6: Off-topic → Bot Refuses**
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"What is 2+2?\"}]}"
```

**Expected:** "I can only help with SHL assessments"

---

### **Option C: Interactive Web UI**

Visit in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Click "Try it out" and test interactively.

---

## 📊 Expected Output Example

When you send:
```json
{
  "messages": [
    {"role": "user", "content": "Hiring a Java developer with communication skills"}
  ]
}
```

You get back:
```json
{
  "reply": "Great! I found relevant assessments for Java developers focusing on technical and communication skills...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "K",
      "description": "Assesses knowledge of..."
    },
    {
      "name": "DACT - Digital",
      "url": "https://www.shl.com/solutions/products/...",
      "test_type": "P",
      "description": "Measures communication..."
    }
    // ... more assessments
  ],
  "end_of_conversation": false
}
```

---

## 🛠️ Troubleshooting

### **"Port 8000 already in use"**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 8001
```

### **"No module named 'sentence_transformers'"**
```bash
pip install -r requirements.txt
```

### **"Cannot connect to localhost:8000"**
- Make sure server is running in another terminal
- Check http://localhost:8000/health

### **"No recommendations returned"**
- Check `data/catalog.json` exists (39 items)
- Check `data/index.pkl` exists
- Verify query has role keywords (Java, Python, QA, etc.)

### **Slow first run**
- First embedding: Downloads model (~100MB) - takes 30-60s
- Cached runs: Much faster

---

## 📁 Project Files

```
d:\SHL\
├── app/
│   ├── main.py                 → FastAPI app with routes
│   ├── core/config.py          → Settings & hyperparameters
│   └── services/
│       ├── catalog.py          → Assessment model
│       ├── recommender.py      → Intent extraction & recommendations
│       ├── retrieval.py        → Semantic search with embeddings
│       ├── comparison.py       → Compare assessments
│       └── guardrails.py       → Prompt injection protection
├── scripts/
│   ├── scrape_catalog.py       → Scrape SHL website (39 tests)
│   └── build_index.py          → Build embedding index
├── data/
│   ├── catalog.json            → SHL assessments (scraped)
│   └── index.pkl               → Embeddings index (generated)
├── requirements.txt            → Python dependencies
├── test_chat.py               → 8 test cases
├── run_project.py             → Python setup script
├── run.bat                    → Windows batch setup script
└── QUICKSTART.md              → Quick reference
```

---

## ✨ Architecture Overview

```
User Query
    ↓
[FastAPI /chat endpoint]
    ↓
[Intent Extraction] (Rule-based, no LLM)
    ├─→ Extract role (Java dev, QA, etc.)
    ├─→ Extract skills (communication, automation, etc.)
    └─→ Determine intent (clarify/recommend/compare)
    ↓
[Semantic Search] (Local embeddings)
    ├─→ Encode query with SentenceTransformers
    ├─→ Search index.pkl for similar assessments
    └─→ Return top-k matches (cosine similarity)
    ↓
[Recommendation Logic]
    ├─→ Filter by role & skills
    ├─→ Rank by relevance
    └─→ Cap at 10 results
    ↓
[Return Response]
    ├─→ reply: Conversational message
    ├─→ recommendations: 1-10 SHL assessments with URLs
    └─→ end_of_conversation: false (continues chat)
```

---

## ⚡ Quick Reference

| Command | Purpose |
|---------|---------|
| `run.bat` | One-click setup (Windows) |
| `python run_project.py` | One-click setup (all platforms) |
| `pip install -r requirements.txt` | Install dependencies |
| `python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl` | Build embeddings |
| `uvicorn app.main:app --port 8000 --reload` | Start server |
| `python test_chat.py` | Run all tests |
| `curl http://localhost:8000/health` | Health check |
| `curl http://localhost:8000/docs` | Swagger UI |

---

## 🎯 What Works

✅ **Conversational** - Multi-turn, full history in each request  
✅ **Semantic Search** - Local embeddings (free, no API)  
✅ **Intent Detection** - Rule-based (deterministic, no hallucinations)  
✅ **Recommendations** - 1-10 SHL assessments with URLs  
✅ **Comparisons** - Compare two assessments  
✅ **Guardrails** - Rejects off-topic & prompt injection  
✅ **Zero API Keys** - Everything runs locally  
✅ **Fast** - <1s per query  
✅ **Stateless** - Full conversation history in each request  

---

## 🚀 Next Steps

1. **Run setup**: `python run_project.py` or `run.bat`
2. **Test API**: `python test_chat.py`
3. **Try manual tests**: Use curl or Swagger UI
4. **Deploy**: See `DEPLOYMENT.md`

---

**Need help?** Check QUICKSTART.md or project README.
