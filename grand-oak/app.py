from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

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
class ReqAppointment(BaseModel):
    patient: str
    doctor: str
    hospital: str

class Doctor(BaseModel):
    name: str
    hospital: str
    category: str
    availability: str
    price: int

class Patient(BaseModel):
    name: str
    dob: str
    address: str
    phone: str
    email: str
    ssn: str

class Appointment(BaseModel):
    patient: str
    doctor: str
    appointment_id: int
    status: str
    payment_id: int
    fee: int


"""
    GENERATE SAMPLE DATA
"""
data_dokter = [
    Doctor(name="Dr. John Doe", hospital="RS. Jakarta", category="Cardiology", availability="8.00 - 15.00", price=100000),
    Doctor(name="Dr. Jane Doe", hospital="RS. Jakarta", category="Tooth", availability="8.00 - 16.00", price=150000),
    Doctor(name="Dr. John Smith", hospital="RS. Jakarta", category="Child", availability="9.00 - 14.00", price=200000),
]

data_pasien = [
    Patient(name="Adi", dob="01-01-2013", address="Jl. Jakarta No. 1", phone="08123456789", email="Adi@gmail.com", ssn="123"),
    Patient(name="Budi", dob="02-02-1991", address="Jl. Jakarta No. 2", phone="08123456788", email="Budi@gmail.com", ssn="124"),
    Patient(name="Cici", dob="03-03-1992", address="Jl. Jakarta No. 3", phone="08123456787", email="Cici@gmail.com", ssn="125"),
]

data_appointment = []


"""
    API ENDPOINTS
"""
@app.post("/{category}/reserve")
async def reserve(category: str, req: ReqAppointment):
    for dokter in data_dokter:
        if dokter.category == category and dokter.hospital == req.hospital and dokter.name == req.doctor:
            appointment = Appointment(
                patient=req.patient,
                doctor=dokter.name,
                appointment_id=len(data_appointment) + 1,
                status="Reserved",
                payment_id=len(data_appointment) + 1,
                fee=dokter.price
            )
            data_appointment.append(appointment)
            return appointment
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.get("/appointments/{appointment_id}/fee")
async def appointment_fee(appointment_id: int):
    for appointment in data_appointment:
        if appointment.appointment_id == appointment_id:
            return appointment.fee
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.get("/patient/{ssn}/getrecord")
async def get_record_patient(ssn: str):
    for pasien in data_pasien:
        if pasien.ssn == ssn:
            return pasien
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/admin/doctor/newdoctor")
async def new_doctor(dokter: Doctor):
    data_dokter.append(dokter)
    return dokter

@app.get("/patient/appointment/{appointment_id}/discount")
async def appointment_discount(appointment_id: int):
    for appointment in data_appointment:
        if appointment.appointment_id == appointment_id:
            for pasien in data_pasien:
                if appointment.patient == pasien.name:
                    year = datetime.now().year
                    year_dob_pasien = int(pasien.dob[6:10])
                    age = year - year_dob_pasien
                    if age > 55 or (age < 12 and age > 0):
                        return "Eligible for discount"
                    else:
                        return "Not eligible for discount"
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.get("/appointments")
async def get_appointment_list():
    return data_appointment

if __name__ == "__main__":
    import uvicorn
    from watchgod import run_process

    run_process('.', lambda: uvicorn.run(app, host="0.0.0.0", port=8081))
