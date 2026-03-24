"""
HealthTrackAI — MongoDB Database Layer
All CRUD for: users, reports, chat_history, health_scores
"""
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from bson import ObjectId
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB  = os.getenv("MONGODB_DB", "healthtrackAI")

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=4000)
    return _client

def get_db():
    return _get_client()[MONGODB_DB]

def ping_db() -> bool:
    try:
        _get_client().admin.command("ping")
        return True
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}", flush=True)
        return False

# ── USERS ──────────────────────────────────────────────────────────────────────

def create_user(username: str, password: str, name: str, email: str = "") -> dict | None:
    """Create a new user with hashed password. Returns user doc or None if exists."""
    db = get_db()
    clean_username = username.strip().lower()
    if not clean_username: return None
        
    if db.users.find_one({"username": clean_username}):
        return None
    
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_id = f"user_{int(datetime.utcnow().timestamp())}"
    
    # Auto-assign Admin role if username/email matches admin secrets
    role = "user"
    admin_user = os.getenv("ADMIN_USERNAME", "").lower()
    admin_email = os.getenv("ADMIN_EMAIL", "").lower()
    
    if (admin_user and clean_username == admin_user) or (admin_email and email.strip().lower() == admin_email):
        role = "admin"
        print(f"Creating ADMIN user: {clean_username}", flush=True)

    doc = {
        "user_id": user_id,
        "username": clean_username,
        "password": hashed,
        "name": name.strip(),
        "email": email.strip().lower(),
        "created_at": datetime.utcnow(),
        "last_active": datetime.utcnow(),
        "age": 0, "gender": "",
        "role": role,
    }
    db.users.insert_one(doc)
    doc.pop("password")
    doc["_id"] = str(doc["_id"])
    return doc

def authenticate_user(username: str, password: str) -> dict | None:
    """Check credentials and return user doc (without password)."""
    clean_username = username.strip().lower()
    user = get_db().users.find_one({"username": clean_username})
    
    # Verify user exists and password matches
    if user:
        # Pymongo returns bytes for Binary fields, ensuring compatibility
        stored_pw = user.get("password")
        if stored_pw and bcrypt.checkpw(password.encode("utf-8"), stored_pw):
            user.pop("password")
            user["_id"] = str(user["_id"])
            return user
    return None

def upsert_user(user_id: str, name: str, email: str = "", age: int = 0, gender: str = "") -> None:
    get_db().users.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"created_at": datetime.utcnow()},
         "$set": {"name": name, "email": email, "age": age, "gender": gender,
                  "last_active": datetime.utcnow()}},
        upsert=True,
    )

def get_user(user_id: str) -> dict | None:
    doc = get_db().users.find_one({"user_id": user_id}, {"_id": 0})
    return doc

# ── REPORTS ────────────────────────────────────────────────────────────────────

def save_report(user_id: str, filename: str, report_type: str,
                raw_text: str, analysis: str, health_score: int,
                breakdown: dict = None) -> str:
    doc = {
        "user_id": user_id,
        "filename": filename,
        "report_type": report_type,
        "raw_text": raw_text[:6000],
        "analysis": analysis,
        "health_score": health_score,
        "breakdown": breakdown or {},
        "uploaded_at": datetime.utcnow(),
    }
    result = get_db().reports.insert_one(doc)
    return str(result.inserted_id)

def get_reports(user_id: str) -> list[dict]:
    cursor = get_db().reports.find(
        {"user_id": user_id},
        {"_id": 1, "filename": 1, "report_type": 1, "health_score": 1,
         "uploaded_at": 1, "analysis": 1, "breakdown": 1}
    ).sort("uploaded_at", DESCENDING)
    result = []
    for d in cursor:
        d["_id"] = str(d["_id"])
        result.append(d)
    return result

def delete_report(report_id: str):
    get_db().reports.delete_one({"_id": ObjectId(report_id)})

# ── CHAT ───────────────────────────────────────────────────────────────────────

def save_message(user_id: str, role: str, content: str, session_id: str = "default") -> None:
    get_db().chat_history.insert_one({
        "user_id": user_id, "session_id": session_id,
        "role": role, "content": content, "timestamp": datetime.utcnow(),
    })

def get_chat_history(user_id: str, session_id: str = "default", limit: int = 60) -> list[dict]:
    cursor = get_db().chat_history.find(
        {"user_id": user_id, "session_id": session_id},
        {"_id": 0, "role": 1, "content": 1, "timestamp": 1}
    ).sort("timestamp", DESCENDING).limit(limit)
    msgs = list(cursor)
    msgs.reverse()
    return msgs

def clear_chat_history(user_id: str, session_id: str = "default") -> None:
    get_db().chat_history.delete_many({"user_id": user_id, "session_id": session_id})

# ── HEALTH SCORES ──────────────────────────────────────────────────────────────

def save_health_score(user_id: str, score: int, breakdown: dict) -> None:
    get_db().health_scores.insert_one({
        "user_id": user_id, "score": score,
        "breakdown": breakdown, "recorded_at": datetime.utcnow(),
    })

def get_health_scores(user_id: str, limit: int = 30) -> list[dict]:
    cursor = get_db().health_scores.find(
        {"user_id": user_id}, {"_id": 0}
    ).sort("recorded_at", DESCENDING).limit(limit)
    scores = list(cursor)
    scores.reverse()
    return scores

def get_latest_health_score(user_id: str) -> dict | None:
    return get_db().health_scores.find_one(
        {"user_id": user_id}, {"_id": 0},
        sort=[("recorded_at", DESCENDING)]
    )

# ── ADMIN & LOGGING ────────────────────────────────────────────────────────────

def log_operation(user_id: str, action: str, details: str = "") -> None:
    """Log user operations for audit trail."""
    get_db().logs.insert_one({
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    })

def get_logs(limit: int = 100) -> list[dict]:
    """Retrieve logs for admin panel."""
    cursor = get_db().logs.find().sort("timestamp", DESCENDING).limit(limit)
    logs = []
    for log in cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)
    return logs

def get_all_users() -> list[dict]:
    """Retrieve all users for admin panel."""
    cursor = get_db().users.find({}, {"password": 0}).sort("created_at", DESCENDING)
    users = []
    for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

def update_user_role(user_id: str, new_role: str) -> None:
    get_db().users.update_one({"user_id": user_id}, {"$set": {"role": new_role}})

def delete_user_full(user_id: str) -> None:
    """Delete a user and all associated data."""
    db = get_db()
    db.users.delete_one({"user_id": user_id})
    db.reports.delete_many({"user_id": user_id})
    db.chat_history.delete_many({"user_id": user_id})
    db.health_scores.delete_many({"user_id": user_id})
    db.logs.delete_many({"user_id": user_id})

def get_system_stats() -> dict:
    db = get_db()
    return {
        "users": db.users.count_documents({}),
        "reports": db.reports.count_documents({}),
        "logs": db.logs.count_documents({}),
        "chats": db.chat_history.count_documents({}),
    }
