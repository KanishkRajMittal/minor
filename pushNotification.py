import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/kanishk/Desktop/Python/firebase/credentials.json")
firebase_admin.initialize_app(cred)
