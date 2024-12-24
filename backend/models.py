from sqlalchemy import Column,Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Table, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Users(Base):
    __tablename__ = "Users"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    users_fname = Column(String(50))
    users_lname = Column(String(50))
    school = Column(String(100))
    major = Column(String(50))
    classification = Column(String(50))
    user_type=Column(String(50))
    email_address=Column(String(100))
    password=Column(String(255))

class Mentees(Base):
    __tablename__ = "Mentees"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    mentor_id = Column(Integer)

class Mentors(Base):
    __tablename__ = "Mentors"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer)

class Admin(Base):
    __tablename__ = "Admin"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    admintype = Column(String(50))

class FYE_Coordinators(Base):
    __tablename__ = "FYE_Coordinators"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer)

class MentoringSession(Base):
    __tablename__ = "MentoringSession"
    sessionid = Column(Integer, primary_key=True, autoincrement=True)
    sessiontitle = Column(String(100))
    deadline=Column(DateTime, server_default=func.now(), nullable=False)
    duration = Column(Integer)
    mandatoryoptional =Column(String(10))

class DateOfSession(Base):
    __tablename__ = "DateOfSession"
    usersid = Column(Integer, primary_key=True, autoincrement=True)
    sessionid = Column(Integer, primary_key=True, autoincrement=True)
    dateofsession=Column(DateTime, server_default=func.now(), nullable=False)

class Event(Base):
    __tablename__ = "Event"
    eventid = Column(Integer, primary_key=True, autoincrement=True)
    sessionid = Column(Integer, primary_key=True, autoincrement=True)
    eventtitle = Column(String(100))
    eventbudget = Column(Integer)

class Date_of_event(Base):
    __tablename__ = "Date_of_event"
    userid = Column(Integer, primary_key=True, autoincrement=True)
    eventid = Column(Integer, primary_key=True, autoincrement=True)
    dateofevent = Column(DateTime, server_default=func.now(), nullable=False)
    timeofevent = Column(TIMESTAMP)
