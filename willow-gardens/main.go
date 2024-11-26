package main

import (
	"net/http"
	"strconv"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type ReqAppointment struct {
	Patient  string `json:"patient"`
	Doctor   string `json:"doctor"`
	Hospital string `json:"hospital"`
}

type Doctor struct {
	Name         string `json:"name"`
	Hospital     string `json:"hospital"`
	Category     string `json:"category"`
	Availibility string `json:"availibility"`
	Price        int    `json:"price"`
}

type Patient struct {
	Name    string `json:"name"`
	DOB     string `json:"dob"`
	Address string `json:"address"`
	Phone   string `json:"phone"`
	Email   string `json:"email"`
	SSN     string `json:"ssn"`
}

type Appointment struct {
	Patient       string `json:"patient"`
	Doctor        string `json:"doctor"`
	AppointmentID int    `json:"appointment_id"`
	Status        string `json:"status"`
	PaymentID     int    `json:"payment_id"`
	Fee           int    `json:"fee"`
}

type AppointmentList struct {
	Appointments []Appointment `json:"appointments"`
}

// array data dokter
var dataDokter = []Doctor{
	{Name: "Dr. John Doe", Hospital: "RS. Jakarta", Category: "Cardiology", Availibility: "8.00 - 15.00", Price: 100000},
	{Name: "Dr. Jane Doe", Hospital: "RS. Jakarta", Category: "Tooth", Availibility: "8.00 - 16.00", Price: 150000},
	{Name: "Dr. John Smith", Hospital: "RS. Jakarta", Category: "Child", Availibility: "9.00 - 14.00", Price: 200000},
}

// array data pasien
var dataPasien = []Patient{
	{Name: "Adi", DOB: "01-01-2013", Address: "Jl. Jakarta No. 1", Phone: "08123456789", Email: "Adi@gmail.com", SSN: "123"},
	{Name: "Budi", DOB: "02-02-1991", Address: "Jl. Jakarta No. 2", Phone: "08123456788", Email: "Budi@gmail.com", SSN: "124"},
	{Name: "Cici", DOB: "03-03-1992", Address: "Jl. Jakarta No. 3", Phone: "08123456787", Email: "Cici@gmail.com", SSN: "125"},
}

// array data appointment
var dataAppointment = []Appointment{}

var mu sync.Mutex

func Reserve(c *gin.Context) {
	category := c.Param("category")
	var req ReqAppointment
	err := c.BindJSON(&req)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	for _, dokter := range dataDokter {
		if dokter.Category == category && dokter.Hospital == req.Hospital && dokter.Name == req.Doctor {
			mu.Lock()
			appointment := Appointment{
				Patient:       req.Patient,
				Doctor:        dokter.Name,
				AppointmentID: len(dataAppointment) + 1,
				Status:        "Reserved",
				PaymentID:     len(dataAppointment) + 1,
				Fee:           dokter.Price,
			}
			dataAppointment = append(dataAppointment, appointment)
			mu.Unlock()
			c.JSON(http.StatusOK, appointment)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "Doctor not found"})
}

func AppointmentFee(c *gin.Context) {
	appointmentID := c.Param("appointment_id")
	appointmentIDint, err := strconv.Atoi(appointmentID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	for _, appointment := range dataAppointment {
		if appointment.AppointmentID == appointmentIDint {
			c.JSON(http.StatusOK, appointment.Fee)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "Appointment not found"})
}

func GetRecordPatient(c *gin.Context) {
	SSN := c.Param("SSN")
	for _, pasien := range dataPasien {
		if pasien.SSN == SSN {
			c.JSON(http.StatusOK, pasien)
			return
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "Patient not found"})
}

func NewDoctor(c *gin.Context) {
	var dokter Doctor
	err := c.BindJSON(&dokter)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	dataDokter = append(dataDokter, dokter)
	c.JSON(http.StatusOK, dokter)
}

func AppointmentDiscount(c *gin.Context) {
	appointmentID := c.Param("appointment_id")
	appointmentIDint, err := strconv.Atoi(appointmentID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	for _, appointment := range dataAppointment {
		if appointment.AppointmentID == appointmentIDint {
			for _, pasien := range dataPasien {
				if appointment.Patient == pasien.Name {
					year, _, _ := time.Now().Date()
					getyeardobpasien, _ := strconv.Atoi(pasien.DOB[6:10])
					if year-getyeardobpasien > 55 {
						c.JSON(http.StatusOK, "Eligible for discount")
					} else if year-getyeardobpasien < 12 && year-getyeardobpasien > 0 {
						c.JSON(http.StatusOK, "Eligible for discount")
					} else {
						c.JSON(http.StatusOK, "Not eligible for discount")
					}
					return
				}
			}
		}
	}
	c.JSON(http.StatusNotFound, gin.H{"error": "Appointment not found"})
}

func GetAppointmentList(c *gin.Context) {
	c.JSON(http.StatusOK, dataAppointment)
}

func main() {
	app := gin.Default()
	app.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST"},
		AllowHeaders:     []string{"Content-Type"},
		AllowCredentials: true,
	}))
	app.POST("/:category/reserve", Reserve)
	app.GET("/appointments/:appointment_id/fee", AppointmentFee)
	app.GET("/patient/:SSN/getrecord", GetRecordPatient)
	app.GET("/admin/doctor/newdoctor", NewDoctor)
	app.GET("/patient/appointment/:appointment_id/discount", AppointmentDiscount)
	app.GET("/appointments", GetAppointmentList)
	app.Run(":8083")
}
