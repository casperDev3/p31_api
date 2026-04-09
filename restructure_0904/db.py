from datetime import datetime
import security
from passlib.context import CryptContext

hash_psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "admin": {
        "email": "admin@example.com",
        "username": "admin",
        "hashed_password": hash_psw_context.hash("admin123"), # admin123
        "is_admin": True,
        "created_at": datetime.utcnow()
    }
}