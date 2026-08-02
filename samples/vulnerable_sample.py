import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

app = FastAPI()

# -------------------------------------------------------------
# FLAW 1: Wildcard CORS (Bypasses local origin issues)
# -------------------------------------------------------------
# Tricked by: "I couldn't get local port 3000 to talk to port 8000."
# Risk: Allows ANY malicious website on the internet to send 
# authenticated API requests from a user's browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # BAD: Should be specific domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# FLAW 2: Hardcoded Fallback Secrets / API Keys
# -------------------------------------------------------------
# Tricked by: "I don't want to export env vars every time I open a terminal."
# Risk: Leakage into GitHub/Git history. Bots automatically scan public repos
# for string patterns like 'JWT_SECRET' or 'mongodb://'.
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_developer_key_12345")
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://admin:pass123@localhost:27017")

# -------------------------------------------------------------
# FLAW 3: Production Debug / Inspect Endpoints
# -------------------------------------------------------------
# Tricked by: "I need an endpoint to check if my local model/RAM loaded fine."
# Risk: Exposes server environment variables, architecture secrets, 
# and memory usage to anyone on the internet.
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.get("/debug-env")
def debug_environment():
    # BAD: Returning raw os.environ leaks API keys, DB strings, and host configs
    return {"status": "ok", "environment": dict(os.environ)}

# -------------------------------------------------------------
# FLAW 4: Bypassing Auth Flags via Query Params
# -------------------------------------------------------------
# Tricked by: "I'm tired of generating a fresh JWT token every time I test Postman."
# Risk: Leaves a back-door bypass in production if forgotten.
@app.post("/chat")
def chat_endpoint(prompt: str, skip_auth: bool = False):
    if not skip_auth:
        # Pretend auth validation logic happens here
        pass
    
    # Process RAG request...
    embedding = model.encode(prompt).tolist()
    return {"status": "success", "embedding_dim": len(embedding)}