import os
import json
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import jwt

# Ρύθμιση Βάσης Δεδομένων
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./parkkarma.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ΜΟΝΤΕΛΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (SQLAlchemy) ---
class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    karma = Column(Integer, default=0)

class SavedLocation(Base):
    __tablename__ = "saved_locations"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

class ParkingSpot(Base):
    __tablename__ = "parking_spots"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    minutes_until_free = Column(Integer)
    photo = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_booked = Column(Boolean, default=False)
    booked_by = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    user_email = Column(String, nullable=True)

class SpotReport(Base):
    __tablename__ = "spot_reports"
    id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(Integer, index=True)
    reporter_id = Column(String)

class KarmaTransaction(Base):
    __tablename__ = "karma_transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    amount = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class OfficialParking(Base):
    __tablename__ = "official_parkings"
    id = Column(Integer, primary_key=True, index=True)
    owner_email = Column(String, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    photo_url = Column(String, nullable=True) # JSON Array
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    hours_weekday = Column(String, default="08:00-21:00")
    hours_saturday = Column(String, default="08:00-15:00")
    hours_sunday = Column(String, default="Κλειστό")
    status = Column(String, default="GREEN") 
    is_closed_today = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ParkKarma API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- PYDANTIC SCHEMAS ---
class AuthRequest(BaseModel):
    id_token: str
    local_spots: Optional[List[dict]] = []

class SpotCreate(BaseModel):
    user_email: Optional[str] = None
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None
    tag: Optional[str] = None
    device_id: Optional[str] = None

class SavedLocationCreate(BaseModel):
    email: str
    latitude: float
    longitude: float

class OfficialParkingCreate(BaseModel):
    owner_email: str
    name: str
    latitude: float
    longitude: float
    photos: Optional[List[str]] = []
    phone: Optional[str] = None
    address: Optional[str] = None
    hours_weekday: str
    hours_saturday: str
    hours_sunday: str

class OfficialParkingStatusUpdate(BaseModel):
    status: str
    is_closed_today: bool

# --- ADMIN EMAIL & SECRET CODE ---
ADMIN_EMAIL = "george@parkkarmaapp.com"
ADMIN_SECRET_CODE = "GEORGE2026"

# --- ENDPOINTS ΓΙΑ ΑΠΛΟΥΣ ΧΡΗΣΤΕΣ ---

@app.post("/auth/google")
async def auth_google(request: AuthRequest, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(request.id_token, options={"verify_signature": False})
        user_email = decoded.get("email")
    except:
        user_email = "test@example.com"

    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(email=user_email, karma=0)
        db.add(user)
        db.commit()
        db.refresh(user)

    for spot in request.local_spots:
        new_saved = SavedLocation(user_email=user_email, latitude=spot['lat'], longitude=spot['lng'])
        db.add(new_saved)
    db.commit()

    saved_locs = db.query(SavedLocation).filter(SavedLocation.user_email == user_email).all()
    saved_list = [{"id": loc.id, "lat": loc.latitude, "lng": loc.longitude} for loc in saved_locs]

    return {"email": user_email, "karma": user.karma, "saved_locations": saved_list}

@app.get("/my-karma/{email}")
async def get_karma(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    karma = user.karma if user else 0
    saved_locs = db.query(SavedLocation).filter(SavedLocation.user_email == email).all()
    saved_list = [{"id": loc.id, "lat": loc.latitude, "lng": loc.longitude} for loc in saved_locs]
    return {"karma": karma, "saved_locations": saved_list}

@app.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    top_users = db.query(User).order_by(User.karma.desc()).limit(10).all()
    leaderboard = [{"user": u.email.split('@')[0], "karma": u.karma} for u in top_users]
    return {"leaderboard": leaderboard}

@app.post("/free-spot")
async def create_free_spot(spot: SpotCreate, db: Session = Depends(get_db)):
    new_spot = ParkingSpot(
        latitude=spot.latitude,
        longitude=spot.longitude,
        minutes_until_free=spot.minutes_until_free,
        photo=spot.photo,
        tag=spot.tag,
        user_email=spot.user_email,
        device_id=spot.device_id,
        created_at=datetime.utcnow()
    )
    db.add(new_spot)
    db.commit()
    db.refresh(new_spot)
    return {"message": "Η θέση δημοσιεύτηκε επιτυχώς", "spot_id": new_spot.id}

@app.get("/search-spots")
async def search_spots(db: Session = Depends(get_db)):
    all_spots = db.query(ParkingSpot).all()
    now = datetime.utcnow()
    active_spots = []
    
    for spot in all_spots:
        time_passed = (now - spot.created_at).total_seconds() / 60
        if time_passed > spot.minutes_until_free:
            db.query(SpotReport).filter(SpotReport.spot_id == spot.id).delete() 
            db.delete(spot)
        else:
            active_spots.append(spot)
    db.commit()

    spots_list = []
    for s in active_spots:
        reports_count = db.query(SpotReport).filter(SpotReport.spot_id == s.id).count()
        if s.user_email:
            user_spots = db.query(ParkingSpot.id).filter(ParkingSpot.user_email == s.user_email).all()
        else:
            user_spots = db.query(ParkingSpot.id).filter(ParkingSpot.device_id == s.device_id).all()
            
        spot_ids = [us.id for us in user_spots]
        user_total_reports = db.query(SpotReport).filter(SpotReport.spot_id.in_(spot_ids)).count() if spot_ids else 0

        spots_list.append({
            "id": s.id,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "minutes_until_free": s.minutes_until_free,
            "photo": s.photo,
            "tag": s.tag,
            "created_at": s.created_at.isoformat() + "Z",
            "is_booked": s.is_booked,
            "booked_by": s.booked_by,
            "device_id": s.device_id,
            "user_email": s.user_email,
            "reports_count": reports_count,
            "user_total_reports": user_total_reports
        })
    return {"spots": spots_list}

@app.post("/report-spot/{spot_id}")
async def report_spot(spot_id: int, reporter_id: str, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε η θέση.")
        
    existing_report = db.query(SpotReport).filter(SpotReport.spot_id == spot_id, SpotReport.reporter_id == reporter_id).first()
    if existing_report:
        return {"message": "Έχεις ήδη αναφέρει αυτή τη θέση."}
        
    new_report = SpotReport(spot_id=spot_id, reporter_id=reporter_id)
    db.add(new_report)
    db.commit()
    return {"message": "Η αναφορά καταχωρήθηκε επιτυχώς!"}

@app.post("/book-spot/{spot_id}")
async def book_spot(spot_id: int, occupier_id: str, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot: raise HTTPException(status_code=404, detail="Η θέση δεν βρέθηκε")
    if spot.is_booked: raise HTTPException(status_code=400, detail="Η θέση είναι ήδη κρατημένη")
    
    spot.is_booked = True
    spot.booked_by = occupier_id
    db.commit()
    return {"message": "Επιτυχής κράτηση"}

@app.post("/unbook-spot/{spot_id}")
async def unbook_spot(spot_id: int, occupier_id: str, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if spot and spot.is_booked and spot.booked_by == occupier_id:
        spot.is_booked = False
        spot.booked_by = None
        db.commit()
        return {"message": "Κράτηση ακυρώθηκε"}
    raise HTTPException(status_code=400, detail="Δεν μπορεί να ακυρωθεί")

@app.delete("/occupy-spot/{spot_id}")
async def occupy_spot(spot_id: int, occupier_email: str, db: Session = Depends(get_db)):
    spot = db.query(ParkingSpot).filter(ParkingSpot.id == spot_id).first()
    if not spot: raise HTTPException(status_code=404, detail="Δεν βρέθηκε")
        
    if spot.user_email and spot.user_email != occupier_email:
        creator = db.query(User).filter(User.email == spot.user_email).first()
        if creator:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            daily_earned = db.query(KarmaTransaction).filter(KarmaTransaction.user_email == creator.email, KarmaTransaction.created_at >= today_start).count() * 10
            if daily_earned < 40:
                creator.karma += 10
                db.add(KarmaTransaction(user_email=creator.email, amount=10, created_at=datetime.utcnow()))
                
    db.delete(spot)
    db.commit()
    return {"message": "Επιτυχία"}

@app.post("/save-location")
async def save_location(loc: SavedLocationCreate, db: Session = Depends(get_db)):
    new_loc = SavedLocation(user_email=loc.email, latitude=loc.latitude, longitude=loc.longitude)
    db.add(new_loc)
    db.commit()
    db.refresh(new_loc)
    return {"id": new_loc.id}

@app.delete("/delete-saved-location/{db_id}")
async def delete_saved_location(db_id: int, db: Session = Depends(get_db)):
    loc = db.query(SavedLocation).filter(SavedLocation.id == db_id).first()
    if loc: db.delete(loc); db.commit()
    return {"message": "Διαγράφηκε"}


# --- ΕΠΙΣΗΜΑ ΠΑΡΚΙΝΓΚ (B2B) ---
@app.get("/official-parkings")
async def get_official_parkings(db: Session = Depends(get_db)):
    parkings = db.query(OfficialParking).all()
    res = []
    for p in parkings:
        photo_list = []
        if p.photo_url:
            try: photo_list = json.loads(p.photo_url)
            except: pass
        res.append({
            "id": p.id,
            "owner_email": p.owner_email,
            "name": p.name,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "photos": photo_list,
            "phone": p.phone,
            "address": p.address,
            "hours_weekday": p.hours_weekday,
            "hours_saturday": p.hours_saturday,
            "hours_sunday": p.hours_sunday,
            "status": p.status,
            "is_closed_today": p.is_closed_today
        })
    return res

@app.post("/admin/official-parking")
async def add_official_parking(parking: OfficialParkingCreate, email: str = Query(...), db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
    
    new_parking = OfficialParking(
        owner_email=parking.owner_email, name=parking.name,
        latitude=parking.latitude, longitude=parking.longitude,
        photo_url=json.dumps(parking.photos), phone=parking.phone,
        address=parking.address, hours_weekday=parking.hours_weekday,
        hours_saturday=parking.hours_saturday, hours_sunday=parking.hours_sunday
    )
    db.add(new_parking)
    db.commit()
    return {"message": "Το Πάρκινγκ προστέθηκε επιτυχώς!"}

@app.put("/admin/official-parking/{p_id}")
async def update_official_parking(p_id: int, parking: OfficialParkingCreate, email: str = Query(...), db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
    p = db.query(OfficialParking).filter(OfficialParking.id == p_id).first()
    if not p: raise HTTPException(status_code=404)
    
    p.owner_email = parking.owner_email
    p.name = parking.name
    p.latitude = parking.latitude
    p.longitude = parking.longitude
    if parking.photos and len(parking.photos) > 0:
        p.photo_url = json.dumps(parking.photos)
    p.phone = parking.phone
    p.address = parking.address
    p.hours_weekday = parking.hours_weekday
    p.hours_saturday = parking.hours_saturday
    p.hours_sunday = parking.hours_sunday
    db.commit()
    return {"message": "Το Πάρκινγκ ενημερώθηκε επιτυχώς!"}

@app.delete("/admin/official-parking/{p_id}")
async def delete_official_parking(p_id: int, email: str = Query(...), secret_code: str = Query(...), db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
    if secret_code != ADMIN_SECRET_CODE: raise HTTPException(status_code=403, detail="Λάθος Κωδικός Ασφαλείας!")
    
    p = db.query(OfficialParking).filter(OfficialParking.id == p_id).first()
    if p:
        db.delete(p)
        db.commit()
    return {"message": "Το Πάρκινγκ διαγράφηκε οριστικά."}

@app.get("/owner/my-parking")
async def get_my_parking(email: str, db: Session = Depends(get_db)):
    parking = db.query(OfficialParking).filter(OfficialParking.owner_email == email).first()
    if not parking: raise HTTPException(status_code=404)
    return parking

@app.put("/owner/update-status")
async def update_parking_status(email: str, update_data: OfficialParkingStatusUpdate, db: Session = Depends(get_db)):
    parking = db.query(OfficialParking).filter(OfficialParking.owner_email == email).first()
    if not parking: raise HTTPException(status_code=404)
    
    parking.status = update_data.status
    parking.is_closed_today = update_data.is_closed_today
    db.commit()
    return {"message": "Η κατάσταση ενημερώθηκε!"}

# --- ADMIN ENDPOINTS (ΧΡΗΣΤΕΣ & ΣΤΑΤΙΣΤΙΚΑ) ---
@app.get("/admin/stats")
async def get_admin_stats(email: str, db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
    return {
        "total_users": db.query(User).count(),
        "active_spots": db.query(ParkingSpot).filter(ParkingSpot.is_booked == False).count(),
        "booked_spots": db.query(ParkingSpot).filter(ParkingSpot.is_booked == True).count(),
        "total_official": db.query(OfficialParking).count()
    }

@app.get("/admin/users-list")
async def get_admin_users_list(email: str, db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
    
    users = db.query(User).all()
    emails_data = []
    for u in users:
        user_spots = db.query(ParkingSpot.id).filter(ParkingSpot.user_email == u.email).all()
        spot_ids = [s.id for s in user_spots]
        reports = db.query(SpotReport).filter(SpotReport.spot_id.in_(spot_ids)).count() if spot_ids else 0
        emails_data.append({"email": u.email, "reports": reports, "karma": u.karma})
        
    anon_spots = db.query(ParkingSpot).filter(ParkingSpot.user_email == None, ParkingSpot.device_id != None).all()
    anon_dict = {}
    for s in anon_spots:
        did = s.device_id
        if did not in anon_dict: anon_dict[did] = 0
        reps = db.query(SpotReport).filter(SpotReport.spot_id == s.id).count()
        anon_dict[did] += reps
        
    anons_data = [{"device_id": k, "reports": v} for k, v in anon_dict.items()]
    
    emails_data.sort(key=lambda x: (-x["reports"], x["email"].lower()))
    anons_data.sort(key=lambda x: (-x["reports"], x["device_id"].lower()))
    
    return {"emails": emails_data, "anons": anons_data}

@app.delete("/admin/ban-user")
async def admin_ban_user(email: str, user_to_ban: str, db: Session = Depends(get_db)):
    if email != ADMIN_EMAIL: raise HTTPException(status_code=403)
        
    if "anon_" in user_to_ban:
        db.query(ParkingSpot).filter(ParkingSpot.device_id == user_to_ban).delete()
        db.commit()
        return {"message": f"Οι θέσεις της ανώνυμης συσκευής διαγράφηκαν."}
    else:
        user = db.query(User).filter(User.email == user_to_ban).first()
        if user:
            db.query(SavedLocation).filter(SavedLocation.user_email == user_to_ban).delete()
            db.query(ParkingSpot).filter(ParkingSpot.user_email == user_to_ban).delete()
            db.query(KarmaTransaction).filter(KarmaTransaction.user_email == user_to_ban).delete()
            db.delete(user)
            db.commit()
        return {"message": f"Ο χρήστης διαγράφηκε επιτυχώς."}

# --- ΦΟΡΤΩΣΗ ΤΗΣ ΙΣΤΟΣΕΛΙΔΑΣ ---
@app.get("/")
async def serve_homepage(): return FileResponse("index.html")

@app.get("/{filename:path}")
async def serve_static_files(filename: str):
    if os.path.isfile(filename): return FileResponse(filename)
    raise HTTPException(status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
