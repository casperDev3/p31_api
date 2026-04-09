from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UpdateProfile, ChangePassword
from security import get_current_user, get_current_admin_user, get_password_hash, verify_password
from db import fake_users_db

router = APIRouter(prefix="/users", tags=["users"])

@router.put(f"/{{username}}")
async def update_profile(username: str, data: UpdateProfile, current_user: dict = Depends(get_current_user)):
    if current_user["username"] != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")
    db_user = fake_users_db.get(username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Update user data
    if data.email:
        db_user["email"] = data.email
    if data.text is not None:
        db_user["text"] = data.text

    return {
        "message": "Profile updated successfully",
        "username": username,
        "email": db_user["email"],
        "text": db_user.get("text", "")
    }
