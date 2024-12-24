from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import Users, Event, Date_of_event
from database import get_db

router = APIRouter()

@router.get("/assigned_events/{coordinator_id}")
def view_assigned_events(coordinator_id: int, db: Session = Depends(get_db)):
    """
    View events assigned to an FYE Coordinator from the Date_of_event table along with all other information.
    """
    assigned_events = (
        db.query(Date_of_event, Event)
        .join(Event, Date_of_event.eventid == Event.eventid)
        .filter(Date_of_event.userid == coordinator_id)
        .all()
    )
    if not assigned_events:
        raise HTTPException(status_code=404, detail="No assigned events found for this coordinator")

    return [
        {
            "event_id": event.eventid,
            "title": event.eventtitle,
            "budget": event.eventbudget,
            "date_of_event": date.dateofevent,
            "time_of_event": date.timeofevent,
        }
        for date, event in assigned_events
    ]


app = FastAPI()
app.include_router(router)

