import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from database import engine, get_db, SessionLocal
import models

# Δημιουργία πινάκων στη βάση
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Επιτρέπουμε όλες τις προσπελάσεις για το frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Σωστό path για το index.html στο Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if not db.query(models.DBUser).filter(models.DBUser.id == 1).first():
        db.add(models.DBUser(id=1, username="default_user", is_pro=False))
        db.commit()
    db.close()

class ParkingSpotCreate(BaseModel):
    user_id: int
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None

@app.get("/")
def read_root():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    else:
        return {"error": f"Το αρχείο index.html δεν βρέθηκε στο {INDEX_FILE}"}

@app.post("/free-spot")
def release_parking_spot(spot: ParkingSpotCreate, db: Session = Depends(get_db)):
    new_spot = models.DBParkingSpot(
        user_id=spot.user_id, 
        latitude=spot.latitude, 
        longitude=spot.longitude, 
        minutes_until_free=spot.minutes_until_free,
        photo=spot.photo
    )
    db.add(new_spot)
    db.commit()
    return {"status": "success"}

@app.get("/search-spots")
def get_active_parking_spots(user_id: int = 1, db: Session = Depends(get_db)):
    all_spots = db.query(models.DBParkingSpot).all()
    spots_data = []
    for spot in all_spots:
        spots_data.append({
            "id": spot.id,
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "minutes_until_free": spot.minutes_until_free,
            "photo": spot.photo,
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
