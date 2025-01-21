from fastapi import APIRouter, HTTPException
from app.controllers.firebase_controller import get_users_from_firebase, add_user_to_firebase, UserCreate
from firebase_admin import auth

router = APIRouter()

@router.get("/users")
def get_users():
    return get_users_from_firebase()

@router.post("/users")
def add_user(user: UserCreate):
    return add_user_to_firebase(user)


@router.delete("/users/{user_id}")
def delete_user_from_firebase(user_id: str):
    try:
        auth.delete_user(user_id)
        return {"message": f"User with ID {user_id} deleted from Firebase"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found in Firebase")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
