# 🎯 THE EXACT CODE TO RUN THIS PROJECT

## Windows Users - Easiest Way

**Step 1:** Open Command Prompt and go to project folder
```cmd
cd d:\SHL
```

**Step 2:** Run this one command
```cmd
run.bat
```

**Done!** Server starts automatically ✅

---

## Any Platform - One Python Command

**Step 1:** Open terminal and go to project folder
```bash
cd d:\SHL
```

**Step 2:** Run this one command
```bash
python run_project.py
```

**Done!** Server starts automatically ✅

---

## If You Want to Do It Manually (All Platforms)

### Terminal 1: Setup and Start Server

Copy-paste these commands one by one:

```bash
cd d:\SHL

pip install -r requirements.txt

python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait until you see:
```
INFO:     Application startup complete
```

✅ Server is now running!

---

### Terminal 2: Run Tests

Open another terminal and run:

```bash
cd d:\SHL

python test_chat.py
```

You'll see:
```
✅ Passed: 8
❌ Failed: 0
🎯 Success Rate: 100.0%

🎉 All tests passed!
```

✅ All tests pass!

---

## Manual API Tests (Terminal 2)

Or test manually with curl:

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected: `{"status": "ok"}`

### Test 2: Get Recommendations
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hiring a Java developer\"}]}"
```

Expected: JSON with recommendations array

### Test 3: Interactive Web UI
Visit: http://localhost:8000/docs

Click "Try it out" and test interactively!

---

## 📊 Expected Output

When everything works, server shows:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Test suite shows:
```
✅ Passed: 8
❌ Failed: 0
🎯 Success Rate: 100.0%
🎉 All tests passed!
```

API response looks like:
```json
{
  "reply": "Great! I found relevant assessments for Java developers...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

## 🛠️ If Something Goes Wrong

### Server won't start - Port 8000 in use
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Then try again:
```bash
uvicorn app.main:app --port 8000 --reload
```

### Tests fail - Server not running
Make sure Terminal 1 shows:
```
INFO:     Application startup complete
```

### No recommendations returned
- Check `data/catalog.json` exists
- Check `data/index.pkl` exists
- Try query with role keyword: "Java", "Python", "QA", etc.

---

## ✅ Verification Steps

1. Run setup: `python run_project.py` or `run.bat`
2. See server message: `Application startup complete` ✅
3. Run tests: `python test_chat.py`
4. See: `Success Rate: 100.0%` ✅
5. Test manually: `curl http://localhost:8000/health`
6. See: `{"status":"ok"}` ✅

**All 6 steps pass?** Project is working! 🎉

---

## Quick Reference

| What | Command |
|------|---------|
| Run (Windows) | `run.bat` |
| Run (Any OS) | `python run_project.py` |
| Setup manually | `pip install -r requirements.txt` |
| Build index | `python scripts/build_index.py --catalog data/catalog.json --index data/index.pkl` |
| Start server | `uvicorn app.main:app --port 8000 --reload` |
| Run tests | `python test_chat.py` |
| Health check | `curl http://localhost:8000/health` |
| API docs | Visit http://localhost:8000/docs |
| API ReDoc | Visit http://localhost:8000/redoc |

---

## 🎉 That's It!

Your project is complete and ready to use.

**No more setup needed. Just run:**
```
python run_project.py
```

Or on Windows:
```
run.bat
```

**Then test:**
```
python test_chat.py
```

Happy coding! 🚀
