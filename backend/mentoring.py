from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.models import Users, Mentees, MentoringSession, DateOfSession
from database import get_db

router = APIRouter()

class CompletedSessionInput(BaseModel):
    mentor_id: int
    session_id: int
    date_of_session: str  # ISO format: "YYYY-MM-DD HH:MM:SS"

@router.get("/mentees/{mentor_id}")
def view_number_of_mentees(mentor_id: int, db: Session = Depends(get_db)):
    #View the number of mentees assigned to a specific mentor.
    mentees = (
        db.query(Mentees)
        .join(Users, Mentees.usersid == Users.usersid)
        .filter(Mentees.mentor_id == mentor_id)
        .all()
    )
    if not mentees:
        raise HTTPException(status_code=404, detail="No mentees found for this mentor")
    return [{"mentee_id": mentee.usersid, "name": f"{mentee.users_fname} {mentee.users_lname}"} for mentee in mentees]

@router.get("/mentoring_sessions/")
def view_mentoring_sessions(db: Session = Depends(get_db)):
    #View all mentoring sessions with details.
    sessions = db.query(MentoringSession).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No mentoring sessions found")
    return [
        {
            "session_id": session.sessionid,
            "title": session.sessiontitle,
            "deadline": session.deadline,
            "duration": session.duration,
            "type": session.mandatoryoptional,
        }
        for session in sessions
    ]

@router.get("/completed_sessions/{mentor_id}")
def completed_sessions(mentor_id: int, db: Session = Depends(get_db)):
    #View completed mentoring sessions for a mentor.
    completed_sessions = (
        db.query(DateOfSession)
        .join(Mentees, DateOfSession.usersid == Mentees.usersid)
        .filter(Mentees.mentor_id == mentor_id)
        .all()
    )
    if not completed_sessions:
        raise HTTPException(status_code=404, detail="No completed sessions found for this mentor")
    return [
        {
            "session_id": session.sessionid,
            "date_of_session": session.dateofsession,
        }
        for session in completed_sessions
    ]

@router.post("/completed_sessions/")
def add_completed_session(session: CompletedSessionInput, db: Session = Depends(get_db)):
    #Add a new completed session to the DateOfSession table.
    
    # Verify the mentor exists
    mentor = db.query(Mentees).filter(Mentees.mentor_id == session.mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    # Verify the session exists
    mentoring_session = db.query(MentoringSession).filter(MentoringSession.sessionid == session.session_id).first()
    if not mentoring_session:
        raise HTTPException(status_code=404, detail="Mentoring session not found")

    # Add the completed session
    new_completed_session = DateOfSession(
        usersid=session.mentor_id,
        sessionid=session.session_id,
        dateofsession=session.date_of_session,
    )
    db.add(new_completed_session)
    db.commit()
    db.refresh(new_completed_session)
    return {"message": "Completed session added successfully", "data": new_completed_session}

app = FastAPI()
app.include_router(router)
