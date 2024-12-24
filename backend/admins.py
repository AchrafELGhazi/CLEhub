from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from backend.models import Users, Mentees, MentoringSession, DateOfSession, Event
from database import get_db

router = APIRouter()

class MentoringSessionUpdate(BaseModel):
    session_id: int
    session_title: str
    deadline: str  
    duration: int
    mandatory_optional: str

class EventUpdate(BaseModel):
    event_id: int
    event_title: str
    event_budget: int

@router.get("/mentees_per_mentor/{mentor_id}")
def mentees_per_mentor(mentor_id: int, db: Session = Depends(get_db)):
    """
    View the list of mentees assigned to a mentor.
    Only accessible to admins with admin_type="Mentor Admin".
    """
    mentees = (
        db.query(Mentees)
        .join(Users, Mentees.usersid == Users.usersid)
        .filter(Mentees.mentor_id == mentor_id)
        .all()
    )
    if not mentees:
        raise HTTPException(status_code=404, detail="No mentees found for this mentor")
    return [
        {"mentee_id": mentee.usersid, "name": f"{mentee.users_fname} {mentee.users_lname}"}
        for mentee in mentees
    ]

@router.get("/mentors_exceeding_deadlines/")
def mentors_exceeding_deadlines(db: Session = Depends(get_db)):
    """
    View mentors who have not completed mentoring sessions before the deadline.
    Returns mentors' emails to allow contacting them.
    """
    overdue_sessions = (
        db.query(Users.email_address)
        .join(Mentees, Mentees.usersid == Users.usersid)
        .join(DateOfSession, DateOfSession.usersid == Mentees.usersid)
        .join(MentoringSession, MentoringSession.sessionid == DateOfSession.sessionid)
        .filter(MentoringSession.deadline < func.now())
        .all()
    )
    if not overdue_sessions:
        raise HTTPException(status_code=404, detail="No mentors exceeding deadlines found")
    return [email for (email,) in overdue_sessions]

@router.put("/update_mentoring_session/")
def update_mentoring_session(session: MentoringSessionUpdate, db: Session = Depends(get_db)):
    """
    Update a mentoring session.
    Only accessible to admins with admin_type="Mentor Admin".
    """
    existing_session = db.query(MentoringSession).filter(MentoringSession.sessionid == session.session_id).first()
    if not existing_session:
        raise HTTPException(status_code=404, detail="Mentoring session not found")
    
    existing_session.sessiontitle = session.session_title
    existing_session.deadline = session.deadline
    existing_session.duration = session.duration
    existing_session.mandatoryoptional = session.mandatory_optional

    db.commit()
    db.refresh(existing_session)
    return {"message": "Mentoring session updated successfully", "data": existing_session}

@router.put("/update_event/")
def update_event(event: EventUpdate, db: Session = Depends(get_db)):
    """
    Update an event.
    Only accessible to admins with admin_type="Event Organizer Admin".
    """
    existing_event = db.query(Event).filter(Event.eventid == event.event_id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    existing_event.eventtitle = event.event_title
    existing_event.eventbudget = event.event_budget

    db.commit()
    db.refresh(existing_event)
    return {"message": "Event updated successfully", "data": existing_event}

app = FastAPI()
app.include_router(router)