from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta, timezone
import asyncio
import requests
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
        await asyncio.sleep(60 * 1) 
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
                        continue
                
                if spot.is_booked and spot.booked_at:
                    booked_time = spot.booked_at
                    if booked_time.tzinfo is None:
                        booked_time = booked_time.replace(tzinfo=timezone.utc)
                    if now > booked_time + timedelta(minutes=5):
                        spot.is_booked = False
                        spot.booked_by = None
                        spot.booked_at = None
            db.commit()
        except Exception as e:
            print(f"Σφάλμα καθαρισμού: {e}")
        finally:
            db.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_expired_spots())

class ParkingSpotCreate(BaseModel):
    user_email: Optional[str] = None
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None
    tag: Optional[str] = None 

class LocalSpot(BaseModel):
    lat: float
    lng: float

class TokenBody(BaseModel):
    id_token: str
    local_spots: Optional[List[LocalSpot]] = []

class SaveLocationBody(BaseModel):
    email: str
    latitude: float
    longitude: float

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/manifest.json")
def get_manifest():
    return FileResponse("manifest.json")

@app.get("/sw.js")
def get_sw():
    return FileResponse("sw.js", media_type="application/javascript")

@app.post("/auth/google")
def google_auth(body: TokenBody, db: Session = Depends(get_db)):
    try:
        google_res = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={body.id_token}")
        if google_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Μη έγκυρο Google Token.")
        
        user_info = google_res.json()
        email = user_info.get("email")
        
        user = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == email).first()
        if not user:
            user = models.DBAppUser(device_id=email, karma=0)
            db.add(user)
            db.commit()
        
        current_saved_count = db.query(models.DBSavedLocation).filter(models.DBSavedLocation.user_email == email).count()
        if body.local_spots:
            for spot in body.local_spots:
                if current_saved_count < 10:
                    db.add(models.DBSavedLocation(user_email=email, latitude=spot.lat, longitude=spot.lng))
                    current_saved_count += 1
            db.commit()
            
        saved_db_locations = db.query(models.DBSavedLocation).filter(models.DBSavedLocation.user_email == email).all()
        saved_list = [{"id": loc.id, "lat": loc.latitude, "lng": loc.longitude} for loc in saved_db_locations]
            
        return {
            "status": "success", 
            "email": email, 
            "karma": user.karma,
            "saved_locations": saved_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/my-karma/{email}")
def get_karma(email: str, db: Session = Depends(get_db)):
    user = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == email).first()
    karma_val = user.karma if user else 0
    
    saved_db_locations = db.query(models.DBSavedLocation).filter(models.DBSavedLocation.user_email == email).all()
    saved_list = [{"id": loc.id, "lat": loc.latitude, "lng": loc.longitude} for loc in saved_db_locations]
    
    return {"karma": karma_val, "saved_locations": saved_list}

@app.post("/save-location")
def save_location(body: SaveLocationBody, db: Session = Depends(get_db)):
    count = db.query(models.DBSavedLocation).filter(models.DBSavedLocation.user_email == body.email).count()
    if count >= 10:
        raise HTTPException(status_code=400, detail="Έχεις φτάσει το μέγιστο όριο των 10 αποθηκευμένων θέσεων!")
    
    new_loc = models.DBSavedLocation(user_email=body.email, latitude=body.latitude, longitude=body.longitude)
    db.add(new_loc)
    db.commit()
    return {"status": "success", "id": new_loc.id}

@app.delete("/delete-saved-location/{loc_id}")
def delete_saved_location(loc_id: int, db: Session = Depends(get_db)):
    loc = db.query(models.DBSavedLocation).filter(models.DBSavedLocation.id == loc_id).first()
    if loc:
        db.delete(loc)
        db.commit()
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Location not found")

@app.post("/free-spot")
def release_parking_spot(spot: ParkingSpotCreate, db: Session = Depends(get_db)):
    new_spot = models.DBParkingSpotV2(
        device_id=spot.user_email if spot.user_email else "anonymous", 
        latitude=spot.latitude, 
        longitude=spot.longitude, 
        minutes_until_free=spot.minutes_until_free,
        photo=spot.photo,
        tag=spot.tag 
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
            "tag": spot.tag, 
            "created_at": spot.created_at.isoformat() if spot.created_at else None,
            "is_booked": spot.is_booked,
            "booked_by": spot.booked_by,
            "booked_at": spot.booked_at.isoformat() if spot.booked_at else None
        })
    return {"spots": spots_data}

@app.post("/book-spot/{spot_id}")
def book_spot(spot_id: int, occupier_id: str, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpotV2).filter(models.DBParkingSpotV2.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε η θέση.")
    if spot.is_booked:
        raise HTTPException(status_code=400, detail="Η θέση είναι ήδη κρατημένη.")
    
    spot.is_booked = True
    spot.booked_by = occupier_id
    spot.booked_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "success"}

@app.post("/unbook-spot/{spot_id}")
def unbook_spot(spot_id: int, occupier_id: str, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpotV2).filter(models.DBParkingSpotV2.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε η θέση.")
    if spot.booked_by == occupier_id:
        spot.is_booked = False
        spot.booked_by = None
        spot.booked_at = None
        db.commit()
    return {"status": "success"}

@app.delete("/occupy-spot/{spot_id}")
def occupy_spot(spot_id: int, occupier_email: str, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpotV2).filter(models.DBParkingSpotV2.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    
    if spot.device_id != "anonymous" and spot.device_id != occupier_email:
        creator = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == spot.device_id).first()
        if creator:
            creator.karma += 10
            
    db.delete(spot)
    db.commit()
    return {"status": "success"}

@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    top_users = db.query(models.DBAppUser).filter(models.DBAppUser.karma > 0).order_by(models.DBAppUser.karma.desc()).limit(10).all()
    
    leaderboard = []
    for user in top_users:
        email = user.device_id
        if "@" in email:
            name_part, domain_part = email.split("@")
            masked_name = name_part[:3] + "***" if len(name_part) > 3 else name_part[:1] + "***"
            masked_email = f"{masked_name}@{domain_part}"
        else:
            masked_email = "Ανώνυμος Οδηγός"
            
        leaderboard.append({"user": masked_email, "karma": user.karma})
        
    return {"leaderboard": leaderboard}
