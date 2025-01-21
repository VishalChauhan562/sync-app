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

def get_users_from_firebase():
    try:
        firebase_users = auth.list_users().users
        return [{"uid": user.uid, "email": user.email, "name": user.display_name} for user in firebase_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_random_name(length=8):
    # Generate a random string of fixed length using letters and digits
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_user_to_firebase():
    try:
        # Generate a random name and append 'firebase' to it
        while True:
            random_name = generate_random_name() + "_firebase"
            # Check if the name already exists in Firebase (based on email)
            existing_user = None
            try:
                existing_user = auth.get_user_by_email(f"{random_name}@example.com")
            except auth.UserNotFoundError:
                pass  # If the user is not found, continue

            if not existing_user:  # If no existing user with the same email, we break out
                break

        # Generate a random email
        random_email = f"{random_name}@example.com"

        # Create a new user in Firebase with the generated data
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        new_user = auth.create_user(
            uid=user_id,
            email=random_email,
            display_name=random_name,
        )

        return {"message": f"User {random_name} added to Firebase successfully", "firebase_user": new_user.uid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
