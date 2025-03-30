from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    Email = Column(String, primary_key=True)
    FirstName = Column(String)
    LastName = Column(String)
    StudentID = Column(String)

    access_logs = relationship("AccessLog", back_populates="user")


class AccessLog(Base):
    __tablename__ = "access_log"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String, ForeignKey("users.Email"))
    SignInTimeExternal = Column(String)
    SignInTime = Column(Float)
    IsMember = Column(Boolean)
    membershipYears = Column(JSON, nullable=False, default=list)

    user = relationship("User", back_populates="access_logs")
    badge_snapshot = relationship("BadgeSnapshot", back_populates="access_log")


class BadgeSnapshot(Base):
    __tablename__ = "badge_snapshot"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Narrative_Detail = Column(String)
    Narrative_Title = Column(String)
    IssuedOn = Column(String)
    CreatedAt = Column(String)
    Revoked = Column(Boolean)
    Revocation_Reason = Column(String)
    BadgeClass = Column(String)
    ImageURL = Column(String)
    AccessLogID = Column(Integer, ForeignKey("access_log.ID"))

    access_log = relationship("AccessLog", back_populates="badge_snapshot")


class LoginRequest(BaseModel):
    Email: str
    FirstName: str
    LastName: str
    SignInTime: str
    StudentID: int
