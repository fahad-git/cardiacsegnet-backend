from fastapi import APIRouter, Body
from models import *
from dbClient import user_handler
from pymongo import DESCENDING

router = APIRouter()


def get_user(username: str):
    user = user_handler.collection.find_one({"username": username})
    if user:
        return user
    return None


def verify_password(plain_password, db_password):
    return plain_password == db_password


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return str(user["id"])


@router.post("/login/")
async def login(user: User):
    user_id = authenticate_user(user.username, user.password)
    if not user_id:
        return {"status": "error", "detail": "Invalid credentials.", "redirect": None}
    return {"status": "success", "detail": "Logged in successfully", "redirect": "/imageDetails/page", "id": user_id}


@router.get("/guest/")
def guest():
    return {"status": "success", "detail": "Logged in as guest", "redirect": "/imageDetails/page", "id": "Guest"}


@router.post("/new/")
async def create_user(new_user: NewUser):
    last_user = user_handler.collection.find_one(sort=[("id", DESCENDING)])
    new_id = last_user["id"] + 1

    existing_user = get_user(new_user.username)
    if existing_user:
        return {"status": "error", "detail": "Username already exists.", "redirect": None}
    
    user_doc = User(id=new_id, username=new_user.username, password=new_user.password)
    
    try:
        user_handler.insert_document(user_doc.model_dump())
        return {"status": "success", "detail": "User created successfully", "id": new_id}
    except Exception as e:
        print(f"Error during incerting: {e}")
        return {"status": "error", "detail": f"Error during user creation: {e}", "redirect": None}

