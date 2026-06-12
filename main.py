from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, timezone
import asyncio
import models
from database import engine, get_db, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")

async def cleanup_expired_spots():
    while True:
        await asyncio.sleep(60 * 5)
        db = SessionLocal()
        try:
            spots = db.query(models.DBParkingSpotV2).all()
            now = datetime.now(timezone.utc)
            for spot in spots:
                if spot.created_at:
                    created = spot.created_at
                    if created.tzinfo is None:
                        created = created.replace(tzinfo=timezone.utc)
                    expiration_time = created + timedelta(minutes=spot.minutes_until_free)
                    if now > expiration_time:
                        db.delete(spot)
            db.commit()
        except Exception as e:
            print(f"Σφάλμα καθαρισμού: {e}")
        finally:
            db.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_expired_spots())

class ParkingSpotCreate(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None

@app.get("/")
def read_root():
    return FileResponse("index.html")

# Endpoint για να παίρνει το frontend τα Karma του χρήστη
@app.get("/my-karma/{device_id}")
def get_karma(device_id: str, db: Session = Depends(get_db)):
    user = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == device_id).first()
    if not user:
        user = models.DBAppUser(device_id=device_id, karma=0)
        db.add(user)
        db.commit()
    return {"karma": user.karma}

@app.post("/free-spot")
def release_parking_spot(spot: ParkingSpotCreate, db: Session = Depends(get_db)):
    # Δημιουργία χρήστη αν δεν υπάρχει
    if not db.query(models.DBAppUser).filter(models.DBAppUser.device_id == spot.device_id).first():
        db.add(models.DBAppUser(device_id=spot.device_id, karma=0))
        
    new_spot = models.DBParkingSpotV2(
        device_id=spot.device_id, 
        latitude=spot.latitude, 
        longitude=spot.longitude, 
        minutes_until_free=spot.minutes_until_free,
        photo=spot.photo
    )
    db.add(new_spot)
    db.commit()
    return {"status": "success"}

@app.get("/search-spots")
def get_active_parking_spots(db: Session = Depends(get_db)):
    all_spots = db.query(models.DBParkingSpotV2).all()
    spots_data = []
    for spot in all_spots:
        spots_data.append({
            "id": spot.id,
            "device_id": spot.device_id,
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "minutes_until_free": spot.minutes_until_free,
            "photo": spot.photo,
            "created_at": spot.created_at.isoformat() if spot.created_at else None
        })
    return {"spots": spots_data}

@app.delete("/occupy-spot/{spot_id}")
def occupy_spot(spot_id: int, occupier_id: str, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpotV2).filter(models.DBParkingSpotV2.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    
    # Η ΛΟΓΙΚΗ ΤΟΥ ΚΑΡΜΑ: Αν αυτός που την παίρνει δεν είναι αυτός που την άφησε
    if spot.device_id != occupier_id:
        creator = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == spot.device_id).first()
        if creator:
            creator.karma += 10
            
    db.delete(spot)
    db.commit()
    return {"status": "success"}
