from datetime import datetime

fake_users_db = {
    "admin": {
        "email": "admin@example.com",
        "username": "admin",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # admin123
        "role": "admin",
        "created_at": datetime.utcnow()
    }
}