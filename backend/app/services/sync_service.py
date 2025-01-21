from firebase_admin import auth
from app.models.database import SessionLocal
from app.models.user import User

def sync_firebase_to_postgres():
    db = SessionLocal()
    try:
        firebase_users = auth.list_users().users
        for user in firebase_users:
            existing_user = db.query(User).filter_by(email=user.email).first()
            if existing_user:
                existing_user.name = user.display_name or "No Name"
                existing_user.user_id = user.uid
            else:
                new_user = User(
                    user_id=user.uid,
                    name=user.display_name or "No Name",
                    email=user.email,
                )
                db.add(new_user)
        db.commit()
        return {"message": "Sync from Firebase to PostgreSQL successful"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()



def sync_postgres_to_firebase():
    db = SessionLocal()
    try:
        postgres_users = db.query(User).all()
        for user in postgres_users:
            try:
                firebase_user = auth.get_user(user.user_id)
                auth.update_user(
                    firebase_user.uid,
                    email=user.email,
                    display_name=user.name,
                )
            except auth.UserNotFoundError:
                auth.create_user(
                    uid=user.user_id,
                    email=user.email,
                    display_name=user.name,
                )
        return {"message": "Sync from PostgreSQL to Firebase successful"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
