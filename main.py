from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch import router as fetch_router
from login import router as login_router
from dbClient import db_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fetch_router, prefix="/api", tags=["Images"])
app.include_router(login_router, prefix="/api", tags=["Authentication"])

db_client.open_connection()
