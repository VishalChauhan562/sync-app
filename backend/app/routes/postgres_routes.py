from fastapi import APIRouter, HTTPException
from app.controllers.postgres_controller import get_users_from_postgres, add_user_to_postgres, UserCreate
from app.models.database import SessionLocal
from app.models.user import User

router = APIRouter()

@router.get("/users")
def get_users():
    return get_users_from_postgres()

@router.post("/users")
def add_user():
    return add_user_to_postgres() 

@router.delete("/users/{user_id}")
def delete_user_from_postgres(user_id: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found in PostgreSQL")
        db.delete(user)
        db.commit()
        return {"message": f"User with ID {user_id} deleted from PostgreSQL"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
