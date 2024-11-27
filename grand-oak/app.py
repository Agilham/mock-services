from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from watchgod import run_process
import uvicorn
import random

app = FastAPI(title="Grand-Oak Hospital API", description="API for Grand-Oak Hospital services")


"""
    CORS CONFIGURATION
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
    MODELS
"""
class Doctor(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    schedule: str
    availability: bool = True

class Room(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    availability: bool = True

class Patient(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str
    contact: str

class Appointment(BaseModel):
    id: Optional[int] = None
    patient_id: int
    doctor_id: int
    room_id: int
    date: str
    time: str
    duration: int   # in minutes
    status: str


"""
    CONSTANTS
"""
categories = ["General", "ICU", "Surgery", "ENT", "Dermatology", "Pediatrics"]
statuses = ["Scheduled", "Completed", "Cancelled", "Missed"]
schedules = [
    "7:00 - 15:00",
    "8:00 - 16:00",
    "9:00 - 17:00",
    "10:00 - 18:00",
    "11:00 - 19:00",
    "12:00 - 20:00",
    "13:00 - 21:00",
]
durations = [30, 60, 90, 120]


"""
    Generate sample data
"""
# Randomly generate 50 doctors, 30 rooms, and 100 patients
doctors = [
    Doctor(id=i, name=f"Dr. {random.choice(['John', 'Jane', 'Mike', 'Emily', 'David', 'Sarah'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'])}",
           category=random.choice(categories), schedule=random.choice(schedules))
    for i in range(1, 51)
]

rooms = [
    Room(id=i, name=f"Room {i}", category=random.choice(categories))
    for i in range(1, 31)
]

patients = [
    Patient(id=i, name=f"{random.choice(['John', 'Jane', 'Mike', 'Emily', 'David', 'Sarah'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'])}",
            age=random.randint(18, 80), gender=random.choice(['Male', 'Female']), contact=f"patient{i}@email.com")
    for i in range(1, 101)
]

# Generate 200 appointments with correct data
appointments = []
for i in range(1, 201):
    status = random.choice(statuses)
    if status == "Scheduled":
        date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    elif status in ["Completed", "Missed"]:
        date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    else:  # Cancelled
        date = (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime("%Y-%m-%d")
    
    # Assign doctor and room with corresponding category
    doctor = next(d for d in doctors if d.category == random.choice(categories))
    room = next(r for r in rooms if r.category == doctor.category)
    appointments.append(Appointment(id=i, patient_id=random.randint(1, 100), doctor_id=doctor.id, room_id=room.id,
                                    date=date, time=f"{random.choice(range(7, 19))}:00", duration=random.choice(durations), status=status)
    )


"""
    HELPER FUNCTIONS
"""
def is_doctor_available(doctor_id: int, date: str, time: str) -> bool:
    doctor_appointments = [a for a in appointments if a.doctor_id == doctor_id and a.date == date and a.status == "Scheduled"]
    appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    for appt in doctor_appointments:
        appt_start = datetime.strptime(f"{appt.date} {appt.time}", "%Y-%m-%d %H:%M")
        appt_end = appt_start + timedelta(minutes=appt.duration)
        if appt_start <= appointment_time < appt_end:
            return False
    return True

def is_room_available(room_id: int, date: str, time: str) -> bool:
    room_appointments = [a for a in appointments if a.room_id == room_id and a.date == date and a.status == "Scheduled"]
    appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    for appt in room_appointments:
        appt_start = datetime.strptime(f"{appt.date} {appt.time}", "%Y-%m-%d %H:%M")
        appt_end = appt_start + timedelta(minutes=appt.duration)
        if appt_start <= appointment_time < appt_end:
            return False
    return True

def update_availability():
    now = datetime.now()
    for doctor in doctors:
        doctor.availability = is_doctor_available(doctor.id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"))
    for room in rooms:
        room.availability = is_room_available(room.id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"))


"""
    API ENDPOINTS
"""
# Root
@app.get("/")
def read_root():
    return {"message": "Welcome to Grand-Oak Hospital API", "version": "1.0"}

# Doctors
@app.get("/doctors", response_model=List[Doctor])
def get_doctors():
    update_availability()
    return doctors

@app.get("/doctors/{doctor_id}", response_model=Doctor)
def get_doctor(doctor_id: int):
    update_availability()
    doctor = next((d for d in doctors if d.id == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.get("/doctors/name/{name}", response_model=Doctor)
def get_doctor_by_name(name: str):
    update_availability()
    name = name.replace("%20", " ")
    doctor = next((d for d in doctors if d.name == name), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.get("/doctors/category/{category}", response_model=List[Doctor])
def get_doctors_by_category(category: str):
    update_availability()
    category = category.replace("%20", " ")
    return [d for d in doctors if d.category == category]

@app.post("/doctors", response_model=Doctor)
def create_doctor(doctor: Doctor):
    # Check if doctor with the same name already exists
    if next((d for d in doctors if d.name == doctor.name), None):
        raise HTTPException(status_code=400, detail="Doctor with the same name already exists")
    doctor.id = max(d.id for d in doctors) + 1
    doctors.append(doctor)
    return doctor

@app.put("/doctors/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: int, doctor_update: Doctor):
    doctor = next((d for d in doctors if d.id == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor.name = doctor_update.name
    doctor.category = doctor_update.category
    doctor.schedule = doctor_update.schedule
    return doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    # Delete doctor from doctors and appointments
    global doctors
    global appointments
    doctors = [d for d in doctors if d.id != doctor_id]
    appointments = [a for a in appointments if a.doctor_id != doctor_id]
    return {"message": "Doctor deleted successfully"}

# Rooms
@app.get("/rooms", response_model=List[Room])
def get_rooms():
    update_availability()
    return rooms

@app.get("/rooms/{room_id}", response_model=Room)
def get_room(room_id: int):
    update_availability()
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.get("/rooms/name/{name}", response_model=Room)
def get_room_by_name(name: str):
    update_availability()
    name = name.replace("%20", " ")
    room = next((r for r in rooms if r.name == name), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.get("/rooms/category/{category}", response_model=List[Room])
def get_rooms_by_category(category: str):
    update_availability()
    category = category.replace("%20", " ")
    return [r for r in rooms if r.category == category]

@app.post("/rooms", response_model=Room)
def create_room(room: Room):
    # Check if room with the same name already exists
    if next((r for r in rooms if r.name == room.name), None):
        raise HTTPException(status_code=400, detail="Room with the same name already exists")
    room.id = max(r.id for r in rooms) + 1
    rooms.append(room)
    return room

@app.put("/rooms/{room_id}", response_model=Room)
def update_room(room_id: int, room_update: Room):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.name = room_update.name
    room.category = room_update.category
    return room

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    # Delete room from rooms and appointments
    global rooms
    global appointments
    rooms = [r for r in rooms if r.id != room_id]
    appointments = [a for a in appointments if a.room_id != room_id]
    return {"message": "Room deleted successfully"}

# Patients
@app.get("/patients", response_model=List[Patient])
def get_patients():
    return patients

@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    patient = next((p for p in patients if p.id == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/name/{name}", response_model=Patient)
def get_patient_by_name(name: str):
    name = name.replace("%20", " ")
    patient = next((p for p in patients if p.name == name), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/patients/age/{age}", response_model=List[Patient])
def get_patients_by_age(age: int):
    return [p for p in patients if p.age == age]

@app.get("/patients/gender/{gender}", response_model=List[Patient])
def get_patients_by_gender(gender: str):
    return [p for p in patients if p.gender == gender]

@app.get("/patients/contact/{contact}", response_model=Patient)
def get_patient_by_contact(contact: str):
    patient = next((p for p in patients if p.contact == contact), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients", response_model=Patient)
def create_patient(patient: Patient):
    patient.id = max(p.id for p in patients) + 1
    patients.append(patient)
    return patient

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient_update: Patient):
    patient = next((p for p in patients if p.id == patient_id), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient.name = patient_update.name
    patient.age = patient_update.age
    patient.gender = patient_update.gender
    patient.contact = patient_update.contact
    return patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    # Delete patient from patients and appointments
    global patients
    global appointments
    patients = [p for p in patients if p.id != patient_id]
    appointments = [a for a in appointments if a.patient_id != patient_id]
    return {"message": "Patient deleted successfully"}

# Appointments
@app.get("/appointments", response_model=List[Appointment])
def get_appointments():
    return appointments

@app.get("/appointments/{appointment_id}", response_model=Appointment)
def get_appointment(appointment_id: int):
    appointment = next((a for a in appointments if a.id == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.get("/appointments/doctors/{doctor_id}", response_model=List[Appointment])
def get_doctor_appointments(doctor_id: int):
    return [a for a in appointments if a.doctor_id == doctor_id]

@app.get("/appointments/rooms/{room_id}", response_model=List[Appointment])
def get_room_appointments(room_id: int):
    return [a for a in appointments if a.room_id == room_id]

@app.get("/appointments/patients/{patient_id}", response_model=List[Appointment])
def get_patient_appointments(patient_id: int):
    return [a for a in appointments if a.patient_id == patient_id]

@app.get("/appointments/status/{status}", response_model=List[Appointment])
def get_appointments_by_status(status: str):
    return [a for a in appointments if a.status == status]

@app.post("/appointments", response_model=Appointment)
def create_appointment(appointment: Appointment):
    if not is_doctor_available(appointment.doctor_id, appointment.date, appointment.time):
        raise HTTPException(status_code=400, detail="Doctor is not available at this time")
    if not is_room_available(appointment.room_id, appointment.date, appointment.time):
        raise HTTPException(status_code=400, detail="Room is not available at this time")
    appointment.id = max(a.id for a in appointments) + 1
    appointments.append(appointment)
    return appointment

@app.put("/appointments/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: int, appointment_update: Appointment):
    appointment = next((a for a in appointments if a.id == appointment_id), None)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if appointment_update.doctor_id != appointment.doctor_id or appointment_update.date != appointment.date or appointment_update.time != appointment.time:
        if not is_doctor_available(appointment_update.doctor_id, appointment_update.date, appointment_update.time):
            raise HTTPException(status_code=400, detail="Doctor is not available at this time")
    if appointment_update.room_id != appointment.room_id or appointment_update.date != appointment.date or appointment_update.time != appointment.time:
        if not is_room_available(appointment_update.room_id, appointment_update.date, appointment_update.time):
            raise HTTPException(status_code=400, detail="Room is not available at this time")
    appointment.patient_id = appointment_update.patient_id
    appointment.doctor_id = appointment_update.doctor_id
    appointment.room_id = appointment_update.room_id
    appointment.date = appointment_update.date
    appointment.time = appointment_update.time
    appointment.duration = appointment_update.duration
    appointment.status = appointment_update.status
    return appointment

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    global appointments
    appointments = [a for a in appointments if a.id != appointment_id]
    return {"message": "Appointment deleted successfully"}

if __name__ == "__main__":
    run_process('.', lambda: uvicorn.run(app, host="0.0.0.0", port=8081))
