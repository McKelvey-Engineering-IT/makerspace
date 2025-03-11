from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    Email = Column(String, primary_key=True)
    Name = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    LastSignIn = Column(Float)

    access_logs = relationship("AccessLog", back_populates="user")
    badge_snapshot = relationship("BadgeSnapshot", back_populates="user", uselist=False)


class AccessLog(Base):
    __tablename__ = "access_log"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String, ForeignKey("users.Email"))
    Name = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    StudentID = Column(String)
    SignInTimeExternal = Column(String)
    SignInTime = Column(Float)
    IsMember = Column(Boolean)

    user = relationship("User", back_populates="access_logs")


class BadgeSnapshot(Base):
    __tablename__ = "badge_snapshot"

    Email = Column(String, ForeignKey("users.Email"), primary_key=True)
    Badges = Column(String)

    user = relationship("User", back_populates="badge_snapshot")


class UserResponse(BaseModel):
    Name: str
    Email: str
    LastSignIn: float

    class Config:
        from_attributes = True


class AccessLogResponse(BaseModel):
    Name: str
    Email: str
    SignInTime: float
    IsMember: bool

    class Config:
        from_attributes = True
