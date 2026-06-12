from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
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

# Background Task για αυτόματο καθαρισμό ληγμένων θέσεων
async def cleanup_expired_spots():
    while True:
        await asyncio.sleep(60 * 5)  # Έλεγχος κάθε 5 λεπτά
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

# Μοντέλα δεδομένων για τα αιτήματα
class ParkingSpotCreate(BaseModel):
    user_email: Optional[str] = None  # Μπορεί να είναι και Null αν είναι ανώνυμος
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None

class TokenBody(BaseModel):
    id_token: str

@app.get("/")
def read_root():
    return FileResponse("index.html")

# endpoint για την επαλήθευση του Google Login
@app.post("/auth/google")
def google_auth(body: TokenBody, db: Session = Depends(get_db)):
    try:
        # Επαληθεύουμε το token απευθείας μέσω του API της Google
        google_res = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={body.id_token}")
        if google_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Μη έγκυρο Google Token.")
        
        user_info = google_res.json()
        email = user_info.get("email")
        
        # Αν ο χρήστης δεν υπάρχει στη βάση, τον δημιουργούμε
        user = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == email).first()
        if not user:
            user = models.DBAppUser(device_id=email, karma=0)
            db.add(user)
            db.commit()
            
        return {"status": "success", "email": email, "karma": user.karma}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Επιστροφή Karma με βάση το Email
@app.get("/my-karma/{email}")
def get_karma(email: str, db: Session = Depends(get_db)):
    user = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == email).first()
    if not user:
        return {"karma": 0}
    return {"karma": user.karma}

@app.post("/free-spot")
def release_parking_spot(spot: ParkingSpotCreate, db: Session = Depends(get_db)):
    new_spot = models.DBParkingSpotV2(
        device_id=spot.user_email if spot.user_email else "anonymous", 
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
def occupy_spot(spot_id: int, occupier_email: str, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpotV2).filter(models.DBParkingSpotV2.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    
    # Απονομή Karma: Μόνο αν η θέση δεν είναι ανώνυμη ΚΑΙ ο occupier δεν είναι ο δημιουργός
    if spot.device_id != "anonymous" and spot.device_id != occupier_email:
        creator = db.query(models.DBAppUser).filter(models.DBAppUser.device_id == spot.device_id).first()
        if creator:
            creator.karma += 10
            
    db.delete(spot)
    db.commit()
    return {"status": "success"}
