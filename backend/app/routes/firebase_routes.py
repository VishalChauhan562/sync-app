from fastapi import APIRouter, HTTPException, Query
from app.controllers.firebase_controller import get_users_from_firebase, add_user_to_firebase, UserCreate
from firebase_admin import auth

router = APIRouter()

@router.get("/users")
def get_users(search_query: str = Query(None, min_length=3)):
    return get_users_from_firebase(search_query)

@router.post("/users")
def add_user():
    return add_user_to_firebase()


@router.delete("/users/{user_id}")
def delete_user_from_firebase(user_id: str):
    try:
        auth.delete_user(user_id)
        return {"message": f"User with ID {user_id} deleted from Firebase"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found in Firebase")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
