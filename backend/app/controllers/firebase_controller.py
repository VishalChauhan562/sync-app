from fastapi import HTTPException
from firebase_admin import auth
from pydantic import BaseModel
import uuid
import random
import string

class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str

def get_users_from_firebase(search_query: str = None):
    try:
        firebase_users = auth.list_users().users
        if search_query:
            firebase_users = [
                user for user in firebase_users
                if search_query.lower() in user.display_name.lower() or search_query.lower() in user.email.lower()
            ]

        sorted_firebase_users = sorted(
            firebase_users, key=lambda user: user.user_metadata.creation_timestamp
        )
        return [{"uid": user.uid, "email": user.email, "name": user.display_name} for user in sorted_firebase_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_random_name(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_user_to_firebase():
    try:
        while True:
            random_name = generate_random_name() + "_firebase"
            existing_user = None
            try:
                existing_user = auth.get_user_by_email(f"{random_name}@example.com")
            except auth.UserNotFoundError:
                pass  

            if not existing_user:  
                break

        random_email = f"{random_name}@example.com"

        user_id = str(uuid.uuid4())  
        new_user = auth.create_user(
            uid=user_id,
            email=random_email,
            display_name=random_name,
        )

        return {"message": f"User {random_name} added to Firebase successfully", "firebase_user": new_user.uid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
