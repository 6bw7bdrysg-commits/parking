from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class DBAppUser(Base):
    __tablename__ = "app_users"
    device_id = Column(String, primary_key=True, index=True) # Το Email
    karma = Column(Integer, default=0)

# ΝΕΟΣ ΠΙΝΑΚΑΣ: Κρατάει έως 10 αποθηκευμένες θέσεις ανά χρήστη
class DBSavedLocation(Base):
    __tablename__ = "saved_locations"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

class DBParkingSpotV2(Base):
    __tablename__ = "parking_spots_v2"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    minutes_until_free = Column(Integer)
    photo = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
