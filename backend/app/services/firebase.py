import firebase_admin
from firebase_admin import credentials, auth
import os

firsbase_creds = os.getenv("FIREBASE_CREDENTIALS_PATH")
cred = credentials.Certificate(firsbase_creds)
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully")
