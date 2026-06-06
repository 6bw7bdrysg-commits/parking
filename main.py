import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from database import engine, get_db, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_FILE = "/opt/render/project/src/index.html"

class ParkingSpotCreate(BaseModel):
    user_id: int
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None
    is_public: bool = True  # Προσθήκη για επιλογή δημοσίευσης

class LoginRequest(BaseModel):
    username: str

@app.get("/")
def read_root():
    return FileResponse(INDEX_FILE)

@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.DBUser).filter(models.DBUser.username == req.username).first()
    if not user:
        user = models.DBUser(username=req.username, is_pro=False)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"user_id": user.id, "username": user.username}

@app.post("/free-spot")
def release_parking_spot(spot: ParkingSpotCreate, db: Session = Depends(get_db)):
    new_spot = models.DBParkingSpot(
        user_id=spot.user_id, 
        latitude=spot.latitude, 
        longitude=spot.longitude, 
        minutes_until_free=spot.minutes_until_free,
        photo=spot.photo,
        is_public=spot.is_public # Αποθήκευση κατάστασης
    )
    db.add(new_spot)
    db.commit()
    return {"status": "success"}

# Νέο endpoint για να γίνει δημόσια μια ιδιωτική θέση
@app.post("/publish-spot/{spot_id}")
def publish_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpot).filter(models.DBParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    spot.is_public = True
    db.commit()
    return {"status": "success"}

@app.get("/search-spots")
def get_active_parking_spots(user_id: int = 1, db: Session = Depends(get_db)):
    # Εμφάνιση όλων των δημόσιων + των ιδιωτικών του ίδιου του χρήστη
    all_spots = db.query(models.DBParkingSpot).filter(
        (models.DBParkingSpot.is_public == True) | (models.DBParkingSpot.user_id == user_id)
    ).all()
    
    spots_data = []
    for spot in all_spots:
        spots_data.append({
            "id": spot.id,
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "minutes_until_free": spot.minutes_until_free,
            "photo": spot.photo,
            "is_public": spot.is_public,
            "user_id": spot.user_id,
            "created_at": spot.created_at.isoformat() if spot.created_at else None
        })
    return {"spots": spots_data}

@app.delete("/occupy-spot/{spot_id}")
def occupy_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpot).filter(models.DBParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    db.delete(spot)
    db.commit()
    return {"status": "success"}
