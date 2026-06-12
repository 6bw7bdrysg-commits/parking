from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    is_pro = Column(Boolean, default=False)

class DBParkingSpot(Base):
    __tablename__ = "parking_spots"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    minutes_until_free = Column(Integer)
    # Προσθήκη στήλης για τη φωτογραφία (αποθηκεύουμε το Base64 string)
    photo = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
