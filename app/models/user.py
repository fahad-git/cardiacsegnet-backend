from pydantic import BaseModel, EmailStr, UUID4, validator, Field
from enum import Enum
from typing import List

class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"

class User(BaseModel):
    id: int
    uuid: UUID4
    name: str
    email: EmailStr
    password: str
    username: str = Field(..., max_length=50)

    @validator('email')
    def validate_email_unique(cls, email):
        # Check if the email is unique in the database.
        # You can add your custom logic here to check uniqueness.
        # For demonstration purposes, we assume it's unique.
        if email_already_exists_in_database(email):
            raise ValueError("Email must be unique")
        return email

    @validator('username')
    def validate_username_unique(cls, username):
        # Check if the username is unique in the database.
        # You can add your custom logic here to check uniqueness.
        # For demonstration purposes, we assume it's unique.
        if username_already_exists_in_database(username):
            raise ValueError("Username must be unique")
        return username

def email_already_exists_in_database(email):
    # Replace this with your database query to check if the email exists.
    # Return True if it exists, False if it's unique.
    # This is a placeholder function.
    existing_emails = ["user1@example.com", "user2@example.com"]
    return email in existing_emails

def username_already_exists_in_database(username):
    # Replace this with your database query to check if the username exists.
    # Return True if it exists, False if it's unique.
    # This is a placeholder function.
    existing_usernames = ["user1", "user2"]
    return username in existing_usernames