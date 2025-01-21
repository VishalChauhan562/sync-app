from fastapi import HTTPException
from firebase_admin import auth
from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str

def get_users_from_firebase():
    try:
        firebase_users = auth.list_users().users
        return [{"uid": user.uid, "email": user.email, "name": user.display_name} for user in firebase_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_user_to_firebase(user: UserCreate):
    try:
        try:
            existing_user = auth.get_user(user.user_id)
            raise HTTPException(status_code=400, detail="User already exists in Firebase")
        except auth.UserNotFoundError:
            new_user = auth.create_user(uid=user.user_id, email=user.email, display_name=user.name)
            return {"message": "User added to Firebase successfully", "firebase_user": new_user.uid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
