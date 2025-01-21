from fastapi import HTTPException, Query
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

def get_users_from_postgres(search_query: str = Query(None, min_length=3)):
    db = SessionLocal()
    try:
        query = db.query(User)
        if search_query:
            query = query.filter(
                (User.name.ilike(f"%{search_query}%")) |
                (User.email.ilike(f"%{search_query}%"))
            )
        users = query.order_by(User.timestamp.desc()).all()
        return users
    finally:
        db.close()

def generate_random_name(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_user_to_postgres():
    db = SessionLocal()
    try:
        while True:
            random_name = generate_random_name() + "_postgres"
            existing_user = db.query(User).filter_by(name=random_name).first()
            if not existing_user:
                break  

        random_email = f"{random_name}@example.com"

        user_id = str(uuid.uuid4()) 
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

