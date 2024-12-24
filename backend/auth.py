from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.models import Users
from database import get_db

router = APIRouter()

class AuthCredentials(BaseModel):
    email_address: str
    password: str

def authenticate(credentials: AuthCredentials, db: Session = Depends(get_db)):
    # Check credentials in the Users table
    user = db.query(Users).filter_by(email_address=credentials.email_address, password=credentials.password).first()
    if user:
        return {"message": "You are logged in", "users_id": user.usersid}
    # If no match found
    raise HTTPException(status_code=401, detail="Invalid email or password")

# Add endpoint for authentication
@router.post("/login")
def login(credentials: AuthCredentials, db: Session = Depends(get_db)):
    return authenticate(credentials, db)

# Create FastAPI app and include the router
app = FastAPI()
app.include_router(router)
