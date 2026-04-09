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


@router.post("/change-password")
async def change_password(data: ChangePassword, current_user: dict = Depends(get_current_user)):
    db_user = fake_users_db.get(current_user["username"])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(data.old_password, db_user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    db_user["hashed_password"] = get_password_hash(data.new_password)
    return {"message": "Password changed successfully"}


@router.get("/system-info", dependencies=[Depends(get_current_admin_user)])
async def get_system_info():
    total_users = len(fake_users_db)
    return {
        "total_users": total_users,
        "system_status": "All systems operational",
        "message": "Admin access granted to system information"
    }
