from fastapi import HTTPException
from app.models.database import SessionLocal
from app.models.user import User
from pydantic import BaseModel

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

def add_user_to_postgres(user: UserCreate):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists in PostgreSQL")
        new_user = User(user_id=user.user_id, name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        return {"message": "User added to PostgreSQL successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
