from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from backend.mentoring import router as mentor_router
from admins import router as admin_router
from backend.fye_coordinator import router as fye_coordinator_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(mentor_router, prefix="/mentor", tags=["Mentor"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(fye_coordinator_router, prefix="/fye_coordinator", tags=["FYE Coordinator"])
