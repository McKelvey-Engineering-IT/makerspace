from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    Email = Column(String, primary_key=True)
    FirstName = Column(String)
    LastName = Column(String)
    StudentID = Column(String)
    # School and ClassLevel REMOVED

    access_logs = relationship("AccessLog", back_populates="user")


class AccessLog(Base):
    __tablename__ = "access_log"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String, ForeignKey("users.Email"))
    SignInTimeExternal = Column(String)
    SignInTime = Column(Float)
    membershipYears = Column(JSON, nullable=False, default=list)
    IsMember = Column(Boolean)
    School = Column(String, nullable=True)        # ADDED
    ClassLevel = Column(String, nullable=True)    # ADDED

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


class EmailException(Base):
    __tablename__ = "email_exceptions"

    exception_email = Column(String(255), primary_key=True)
    badgr_email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class LoginRequest(BaseModel):
    Email: str
    FirstName: str
    LastName: str
    SignInTime: str
    StudentID: int
    School: Optional[str] = None
    ClassLevel: Optional[str] = None
