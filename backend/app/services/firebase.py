import firebase_admin
from firebase_admin import credentials, auth
import os
import json

firsbase_creds = os.getenv("FIREBASE_CREDENTIALS_PATH")
creds_dict = json.loads(firsbase_creds)
cred = credentials.Certificate(creds_dict)
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully")
