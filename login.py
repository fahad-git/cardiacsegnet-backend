from fastapi import APIRouter, Body
from models import *
from dbClient import user_handler

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
    return user


@router.post("/login/")
async def login(user: User):
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        return {"status": "error", "detail": "Invalid credentials.", "redirect": None}
    return {"status": "success", "detail": "Logged in successfully", "redirect": "/imageDetails/page"}


@router.get("/guest/")
def guest():
    return {"status": "success", "detail": "Logged in as guest", "redirect": "/imageDetails/page"}


@router.post("/new/")
async def create_user(id:int, username: str, password: str = Body(..., embed=True, alias="password")):
    
    user_doc = User(id=id, username=username, password=password)

    user_handler.collection.insert_one(user_doc.model_dump())
    
    return {"detail": "User created successfully", "redirect": "/imageDetails/page"}

