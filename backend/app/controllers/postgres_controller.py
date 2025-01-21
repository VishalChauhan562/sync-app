from fastapi import HTTPException
from app.models.database import SessionLocal
from app.models.user import User
from pydantic import BaseModel
import uuid
import random
import string

class UserCreate(BaseModel):
    user_id: str
    name: str
    email: str

def get_users_from_postgres():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        return users
    finally:
        db.close()

def generate_random_name(length=8):
    # Generate a random string of fixed length using letters and digits
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_user_to_postgres():
    db = SessionLocal()
    try:
        # Generate a random name and append 'postgres' to it
        while True:
            random_name = generate_random_name() + "_postgres"
            # Check if the name already exists in the database
            existing_user = db.query(User).filter_by(name=random_name).first()
            if not existing_user:
                break  # Name is unique, exit the loop

        # Generate a random email
        random_email = f"{random_name}@example.com"

        # Create a new user with a random name and email
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        new_user = User(
            user_id=user_id,
            name=random_name,
            email=random_email
        )
        db.add(new_user)
        db.commit()

        return {"message": f"User {random_name} added to PostgreSQL successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

