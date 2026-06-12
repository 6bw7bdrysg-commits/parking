from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

# Νέος πίνακας χρηστών για αποθήκευση Karma
class DBAppUser(Base):
    __tablename__ = "app_users"
    device_id = Column(String, primary_key=True, index=True)
    karma = Column(Integer, default=0)

# Νέος πίνακας θέσεων που δέχεται το string του device_id
class DBParkingSpotV2(Base):
    __tablename__ = "parking_spots_v2"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True) # Ποιος την ανέβασε
    latitude = Column(Float)
    longitude = Column(Float)
    minutes_until_free = Column(Integer)
    photo = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
