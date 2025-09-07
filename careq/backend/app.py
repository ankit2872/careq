import os
from datetime import datetime, timedelta
from typing import List, Dict
import json

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import httpx
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from starlette.responses import FileResponse

from .db import init_db, get_db, Patient, calculate_dynamic_eta
from .triage import get_triage_score, get_severity_level
from .ai_predictor import ai_predictor
from .gemini_ai import gemini_ai
load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
LANG_DEFAULT = os.getenv("LANG_DEFAULT", "en")

app = FastAPI()
scheduler = AsyncIOScheduler()

i18n_data: Dict[str, Dict[str, str]] = {}

def load_i18n():
    for lang_file in os.listdir("backend/i18n"):
        if lang_file.endswith(".json"):
            lang_code = lang_file.split(".")[0]
            with open(f"backend/i18n/{lang_file}", 'r', encoding='utf-8') as f:
                i18n_data[lang_code] = json.load(f)

load_i18n()

def get_text(key: str, lang_code: str = LANG_DEFAULT, **kwargs) -> str:
    lang_code = lang_code if lang_code in i18n_data else LANG_DEFAULT
    text = i18n_data.get(lang_code, {}).get(key, i18n_data.get(LANG_DEFAULT, {}).get(key, key))
    return text.format(**kwargs)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    init_db()
    if not scheduler.running:
        scheduler.start()

class PatientCreate(BaseModel):
    user_id: int  # Changed from telegram_id to user_id for web compatibility
    name: str
    age: int
    symptoms: List[str]
    lang_code: str = LANG_DEFAULT

class PatientUpdate(BaseModel):
    called: bool

@app.post("/patients/", response_model=dict)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Check if patient already exists
    db_patient = db.query(Patient).filter(Patient.user_id == patient.user_id).first()

    triage_score = get_triage_score(patient.symptoms, patient.age)
    severity_level = get_severity_level(triage_score)
    
    # Get current queue for AI prediction
    current_patients = db.query(Patient).filter(Patient.called == False).all()
    current_queue = [
        {
            'id': p.id,
            'severity_level': p.severity_level,
            'called': p.called,
            'eta': p.eta
        } for p in current_patients
    ]
    
    # Use AI to predict waiting time
    patient_data = {
        'severity_level': severity_level,
        'symptoms': patient.symptoms,
        'age': patient.age
    }
    
    ai_prediction = ai_predictor.predict_waiting_time(patient_data, current_queue)
    eta = ai_prediction['predicted_wait_time']

    if db_patient:
        # Update existing patient
        db_patient.name = patient.name
        db_patient.age = patient.age
        db_patient.symptoms = json.dumps(patient.symptoms)
        db_patient.triage_score = triage_score
        db_patient.severity_level = severity_level
        db_patient.eta = eta
        db_patient.lang_code = patient.lang_code
        db.commit()
        db.refresh(db_patient)
    else:
        # Create new patient
        db_patient = Patient(
            user_id=patient.user_id,
            name=patient.name,
            age=patient.age,
            symptoms=json.dumps(patient.symptoms),
            triage_score=triage_score,
            severity_level=severity_level,
            eta=eta,
            lang_code=patient.lang_code,
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

    # Broadcast queue update via WebSocket
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/patients/")
        response.raise_for_status()
        all_patients = response.json()
        await manager.broadcast(json.dumps({"type": "queue_update", "patients": all_patients}))

    await reschedule_queue_notifications(db)

    return {"id": db_patient.id, "eta": eta, "severity": severity_level}

@app.get("/patients/", response_model=List[dict])
async def get_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).order_by(Patient.triage_score.desc(), Patient.queued_at.asc()).all()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "name": p.name,
            "age": p.age,
            "symptoms": json.loads(p.symptoms),
            "triage_score": p.triage_score,
            "severity_level": p.severity_level,
            "eta": p.eta,
            "queued_at": p.queued_at.isoformat(),
            "called": p.called,
        }
        for p in patients
    ]

@app.put("/patients/{patient_id}", response_model=dict)
async def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db_patient.called = patient_update.called
    db.commit()
    db.refresh(db_patient)

    # Broadcast queue update via WebSocket
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/patients/")
        response.raise_for_status()
        all_patients = response.json()
        await manager.broadcast(json.dumps({"type": "queue_update", "patients": all_patients}))

    await reschedule_queue_notifications(db)

    return {"id": db_patient.id, "called": db_patient.called}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, can also receive messages from frontend if needed
            data = await websocket.receive_text()
            # Optionally handle incoming messages, e.g., keep-alive pings
            # await manager.send_personal_message(f"You sent: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client disconnected: {websocket.client}")

@app.get("/i18n/{key}", response_model=dict)
async def get_i18n_message(key: str, lang_code: str = LANG_DEFAULT):
    return {"text": get_text(key, lang_code)}

@app.get("/", response_class=HTMLResponse)
async def read_home():
    with open("frontend/index.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/patient-form", response_class=HTMLResponse)
async def read_patient_form():
    with open("frontend/patient_form.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/admin", response_class=HTMLResponse)
async def read_admin_dashboard():
    with open("frontend/admin.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/admin-dashboard", response_class=HTMLResponse)
async def read_advanced_admin_dashboard():
    with open("frontend/admin_dashboard.html", 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/ai/queue-analytics")
async def get_queue_analytics(db: Session = Depends(get_db)):
    """Get AI-powered queue analytics"""
    patients = db.query(Patient).all()
    current_queue = [
        {
            'id': p.id,
            'severity_level': p.severity_level,
            'called': p.called,
            'eta': p.eta,
            'queued_at': p.queued_at.isoformat() if p.queued_at else None
        } for p in patients
    ]
    
    analytics = ai_predictor.get_queue_analytics(current_queue)
    return analytics

@app.get("/ai/predict-wait-time")
async def predict_wait_time(
    severity_level: str,
    symptoms: str,
    age: int,
    db: Session = Depends(get_db)
):
    """Predict waiting time for a potential patient"""
    # Get current queue
    current_patients = db.query(Patient).filter(Patient.called == False).all()
    current_queue = [
        {
            'id': p.id,
            'severity_level': p.severity_level,
            'called': p.called,
            'eta': p.eta
        } for p in current_patients
    ]
    
    # Parse symptoms
    symptoms_list = [s.strip() for s in symptoms.split(',')]
    
    patient_data = {
        'severity_level': severity_level,
        'symptoms': symptoms_list,
        'age': age
    }
    
    prediction = ai_predictor.predict_waiting_time(patient_data, current_queue)
    return prediction

@app.get("/ai/patient-analysis/{patient_id}")
async def get_patient_ai_analysis(patient_id: int, db: Session = Depends(get_db)):
    """Get AI analysis for a specific patient"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = {
        'id': patient.id,
        'name': patient.name,
        'age': patient.age,
        'symptoms': json.loads(patient.symptoms) if isinstance(patient.symptoms, str) else patient.symptoms,
        'severity_level': patient.severity_level,
        'triage_score': patient.triage_score,
        'eta': patient.eta
    }
    
    # Get AI analysis
    analysis = await gemini_ai.analyze_patient_symptoms(patient_data)
    recommendations = await gemini_ai.generate_treatment_recommendations(patient_data)
    insights = await gemini_ai.generate_health_insights(patient_data)
    
    return {
        'patient_id': patient_id,
        'patient_data': patient_data,
        'ai_analysis': analysis,
        'treatment_recommendations': recommendations,
        'health_insights': insights
    }

@app.get("/ai/queue-insights")
async def get_queue_ai_insights(db: Session = Depends(get_db)):
    """Get AI insights for the entire queue"""
    patients = db.query(Patient).all()
    patient_list = [
        {
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'symptoms': json.loads(p.symptoms) if isinstance(p.symptoms, str) else p.symptoms,
            'severity_level': p.severity_level,
            'triage_score': p.triage_score,
            'eta': p.eta,
            'called': p.called,
            'queued_at': p.queued_at.isoformat() if p.queued_at else None
        } for p in patients
    ]
    
    # Get AI queue analysis
    queue_analysis = await gemini_ai.analyze_queue_patterns(patient_list)
    
    return {
        'total_patients': len(patients),
        'queue_analysis': queue_analysis,
        'timestamp': datetime.now().isoformat()
    }

@app.post("/ai/analyze-symptoms")
async def analyze_symptoms_ai(request: dict):
    """Analyze symptoms using Gemini AI"""
    symptoms = request.get('symptoms', [])
    age = request.get('age', 0)
    severity_level = request.get('severity_level', 'Medium')
    
    patient_data = {
        'symptoms': symptoms,
        'age': age,
        'severity_level': severity_level
    }
    
    analysis = await gemini_ai.analyze_patient_symptoms(patient_data)
    recommendations = await gemini_ai.generate_treatment_recommendations(patient_data)
    
    return {
        'symptoms': symptoms,
        'age': age,
        'severity_level': severity_level,
        'ai_analysis': analysis,
        'treatment_recommendations': recommendations
    }

@app.get("/generate_token_pdf/{patient_id}")
async def generate_token_pdf(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Create a more descriptive filename
    pdf_filename = f"CareQ_Token_{patient_id}_{patient.name.replace(' ', '_')}.pdf"
    
    # Use A4 size for better compatibility
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # Header with gradient-like effect
    c.setFillColorRGB(0.4, 0.5, 0.9)  # Blue color
    c.rect(0, height - 80, width, 80, fill=1)
    
    # White text on blue background
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(50, height - 50, "🏥 CareQ Patient Token")
    
    # Token number prominently displayed
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(50, height - 120, f"Token #{patient.id}")

    # Patient information section
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 180, "Patient Information")
    
    # Draw a line under the header
    c.line(50, height - 190, width - 50, height - 190)
    
    c.setFont("Helvetica", 14)
    y_position = height - 220
    
    # Patient details with better formatting
    details = [
        ("Name:", patient.name),
        ("Age:", f"{patient.age} years"),
        ("Symptoms:", ', '.join(json.loads(patient.symptoms))),
        ("Severity Level:", patient.severity_level),
        ("Estimated Wait Time:", f"{patient.eta} minutes"),
        ("Registration Time:", patient.queued_at.strftime("%Y-%m-%d %H:%M:%S"))
    ]
    
    for label, value in details:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y_position, label)
        c.setFont("Helvetica", 12)
        c.drawString(150, y_position, str(value))
        y_position -= 25

    # Generate QR Code with better positioning
    qr_data = f"CareQ Token #{patient.id}\nPatient: {patient.name}\nWait Time: {patient.eta} minutes"
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=8, 
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code to a temporary file
    qr_filename = f"temp_qr_{patient_id}.png"
    img.save(qr_filename)

    # Draw QR code on PDF with better positioning
    qr_size = 120
    qr_x = width - qr_size - 50
    qr_y = height - 400
    c.drawImage(qr_filename, qr_x, qr_y, width=qr_size, height=qr_size)
    
    # Add QR code label
    c.setFont("Helvetica-Bold", 12)
    c.drawString(qr_x, qr_y - 20, "Scan for Details")
    
    # Footer
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 50, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 35, "CareQ Healthcare Queue Management System")
    
    # Clean up temporary QR code image
    try:
        os.remove(qr_filename)
    except OSError:
        pass  # File might not exist

    c.save()

    return FileResponse(
        path=pdf_filename, 
        filename=pdf_filename, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={pdf_filename}"}
    )

async def reschedule_queue_notifications(db: Session):
    """
    Manages and reschedules 'next in queue' notifications based on the current queue.
    """
    # Clear all existing 'next in queue' jobs
    for job in scheduler.get_jobs():
        if job.id.startswith("notify_"):
            scheduler.remove_job(job.id)

    # Get uncalled patients, ordered by priority
    patients_in_queue = db.query(Patient).filter(Patient.called == False)
    patients_in_queue = patients_in_queue.order_by(Patient.triage_score.desc(), Patient.queued_at.asc()).all()

    # Notify the first N patients (e.g., top 3) whose turn is approaching
    NOTIFICATION_WINDOW = 3 # Notify the top 3 patients
    for i, patient in enumerate(patients_in_queue[:NOTIFICATION_WINDOW]):
        # Schedule notification for a few minutes before their estimated turn
        # This is a simplified calculation, real-world ETA would be more complex
        notification_time = datetime.now() + timedelta(minutes=patient.eta - 5) # Notify 5 mins before ETA
        if notification_time < datetime.now():
            notification_time = datetime.now() + timedelta(seconds=30) # Ensure it's in the future

        async def send_next_notification_closure(p_id=patient.id, p_user_id=patient.user_id, p_lang_code=patient.lang_code):
            # For web interface, we can implement email/SMS notifications here
            # For now, we'll just log the notification
            print(f"Notification: Patient {p_id} (User ID: {p_user_id}) is next in queue")

        scheduler.add_job(
            send_next_notification_closure,
            DateTrigger(run_date=notification_time),
            id=f"notify_{patient.id}",
            replace_existing=True # Replace if a job with this ID already exists
        )
