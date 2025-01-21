from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI,HTTPException
from app.models.database import Base, engine
from app.routes.postgres_routes import router as postgres_router
from app.routes.firebase_routes import router as firebase_router
from app.services.sync_service import sync_firebase_to_postgres, sync_postgres_to_firebase
from app.services.firebase import firebase_admin


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Running...."}

app.include_router(postgres_router, prefix="/postgres", tags=["PostgreSQL"])
app.include_router(firebase_router, prefix="/firebase", tags=["Firebase"])

@app.post("/sync/firebase-to-postgres")
def firebase_to_postgres():
    result = sync_firebase_to_postgres()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.post("/sync/postgres-to-firebase")
def postgres_to_firebase():
    result = sync_postgres_to_firebase()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
