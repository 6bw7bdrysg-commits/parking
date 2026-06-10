import os
import datetime
import smtplib
import re
import random
from email.mime.text import MIMEText

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

# Χρησιμοποιούμε το werkzeug για ασφαλή κρυπτογράφηση κωδικών
from werkzeug.security import generate_password_hash, check_password_hash

from database import engine, get_db, SessionLocal
import models

# Δημιουργία των πινάκων στη βάση αν δεν υπάρχουν
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Εφόσον το βρήκαμε στη ρίζα, ορίζουμε το path έτσι:
INDEX_FILE = "/opt/render/project/src/index.html"


# --- PYDANTIC SCHEMAS ---

class ParkingSpotCreate(BaseModel):
    user_id: int
    latitude: float
    longitude: float
    minutes_until_free: int
    photo: Optional[str] = None

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PasswordReset(BaseModel):
    email: str

class EmailVerification(BaseModel):
    email: str
    code: str


# --- STARTUP EVENT ---

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    if not db.query(models.DBUser).filter(models.DBUser.id == 1).first():
        default_password = generate_password_hash("123456")
        db.add(models.DBUser(id=1, email="admin@parkkarma.com", password_hash=default_password, is_verified=True))
        db.commit()
    db.close()


# --- ROUTES ---

@app.get("/")
def read_root():
    return FileResponse(INDEX_FILE)


# 1. ΕΓΓΡΑΦΗ ΜΕ ΑΠΟΣΤΟΛΗ ΚΩΔΙΚΟΥ ΕΠΙΒΕΒΑΙΩΣΗΣ
@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    email_lower = user.email.strip().lower()
    
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(email_regex, email_lower):
        return JSONResponse(status_code=400, content={"error": "Μη έγκυρη μορφή email."})
    
    existing_user = db.query(models.DBUser).filter(models.DBUser.email == email_lower).first()
    if existing_user:
        return JSONResponse(status_code=400, content={"error": "Το email χρησιμοποιείται ήδη."})
    
    v_code = str(random.randint(100000, 999999))
    hashed_password = generate_password_hash(user.password)
    
    new_user = models.DBUser(
        email=email_lower, 
        password_hash=hashed_password,
        is_verified=False,
        verification_code=v_code
    )
    db.add(new_user)
    db.commit()
    
    # ΑΠΟΣΤΟΛΗ EMAIL
    try:
        sender_email = "your-app-email@gmail.com" # ΑΛΛΑΞΕ ΤΟ
        sender_password = "your-app-password"      # ΑΛΛΑΞΕ ΤΟ (App Password)
        
        msg = MIMEText(f"Ο κωδικός επιβεβαίωσης για το ParkKarma είναι: {v_code}")
        msg['Subject'] = 'Επιβεβαίωση Εγγραφής - ParkKarma'
        msg['From'] = sender_email
        msg['To'] = email_lower
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_lower, msg.as_string())
    except Exception as e:
        print(f"Σφάλμα αποστολής email: {e}")
        return JSONResponse(status_code=500, content={"error": "Επιτυχής εγγραφή, αλλά απέτυχε η αποστολή email."})
    
    return {"message": "Επιτυχής εγγραφή! Ελέγξτε το email σας για τον κωδικό επιβεβαίωσης."}


# 1.1 ΕΠΙΒΕΒΑΙΩΣΗ EMAIL
@app.post("/verify")
def verify_user(data: EmailVerification, db: Session = Depends(get_db)):
    user = db.query(models.DBUser).filter(models.DBUser.email == data.email.lower()).first()
    if user and user.verification_code == data.code:
        user.is_verified = True
        user.verification_code = None
        db.commit()
        return {"message": "Ο λογαριασμός επιβεβαιώθηκε!"}
    return JSONResponse(status_code=400, content={"error": "Λάθος κωδικός επιβεβαίωσης."})


# 2. ΕΙΣΟΔΟΣ
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    email_lower = user.email.strip().lower()
    db_user = db.query(models.DBUser).filter(models.DBUser.email == email_lower).first()
    
    if not db_user or not check_password_hash(db_user.password_hash, user.password):
        return JSONResponse(status_code=401, content={"error": "Λάθος email ή κωδικός."})
    
    if not db_user.is_verified:
        return JSONResponse(status_code=403, content={"error": "Πρέπει πρώτα να επιβεβαιώσετε το email σας."})
    
    return {"message": "Επιτυχής σύνδεση!", "user_id": db_user.id}


# 3. ΕΠΑΝΑΦΟΡΑ ΚΩΔΙΚΟΥ
@app.post("/reset-password-request")
def reset_password_request(req: PasswordReset, db: Session = Depends(get_db)):
    email_lower = req.email.strip().lower()
    user = db.query(models.DBUser).filter(models.DBUser.email == email_lower).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "Δεν βρέθηκε λογαριασμός."})
    
    try:
        sender_email = "your-app-email@gmail.com" 
        sender_password = "your-app-password"    
        temporary_password = f"Park{datetime.datetime.now().strftime('%S%M')}"
        user.password_hash = generate_password_hash(temporary_password)
        db.commit()
        
        msg = MIMEText(f"Ο νέος κωδικός σας είναι: {temporary_password}")
        msg['Subject'] = 'Επαναφορά Κωδικού - ParkKarma'
        msg['From'] = sender_email
        msg['To'] = email_lower
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email_lower, msg.as_string())
            
        return {"message": "Το email επαναφοράς στάλθηκε!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Αποτυχία αποστολής."})


# 4. ΔΗΜΙΟΥΡΓΙΑ ΘΕΣΗΣ
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


# 5. ΑΝΑΖΗΤΗΣΗ ΘΕΣΕΩΝ
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


# 6. ΔΙΑΓΡΑΦΗ ΘΕΣΗΣ
@app.delete("/occupy-spot/{spot_id}")
def occupy_spot(spot_id: int, db: Session = Depends(get_db)):
    spot = db.query(models.DBParkingSpot).filter(models.DBParkingSpot.id == spot_id).first()
    if not spot:
        raise HTTPException(status_code=404, detail="Δεν βρέθηκε.")
    db.delete(spot)
    db.commit()
    return {"status": "success"}
