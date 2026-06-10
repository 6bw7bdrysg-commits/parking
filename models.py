from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class DBUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_pro = Column(Boolean, default=False)
    karma_points = Column(Integer, default=0)
    
    # Πεδία για την επιβεβαίωση email
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)

class DBParkingSpot(Base):
    __tablename__ = "parking_spots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    minutes_until_free = Column(Integer, nullable=False)
    photo = Column(String, nullable=True) 
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
