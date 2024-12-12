"use client";

import styles from "./page.module.css";
import { useState } from "react";

const doctorData = {
  "grand-oak": [
    {
      name: "budi",
      category: "cardiology",
      availability: "8.00 - 15.00",
      price: 100000,
    },
    {
      name: "arie",
      category: "tooth",
      availability: "8.00 - 16.00",
      price: 150000,
    },
    {
      name: "gunawan",
      category: "child",
      availability: "9.00 - 14.00",
      price: 200000,
    },
  ],
  "pine-valley": [
    {
      name: "seth mears",
      category: "surgery",
      availability: "3.00 p.m - 5.00 p.m",
      price: 8000,
    },
    {
      name: "emeline fulton",
      category: "cardiology",
      availability: "8.00 a.m - 10.00 a.m",
      price: 4000,
    },
  ],
  "willow-gardens": [
    {
      name: "john doe",
      category: "cardiology",
      availability: "8.00 - 15.00",
      price: 100000,
    },
    {
      name: "jane doe",
      category: "tooth",
      availability: "8.00 - 16.00",
      price: 150000,
    },
    {
      name: "john smith",
      category: "child",
      availability: "9.00 - 14.00",
      price: 200000,
    },
  ],
};

export default function Home() {
  const [doctors, setDoctors] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [reservationStatus, setReservationStatus] = useState(null);

  const fetchDoctors = () => {
    const allDoctors = [
      ...doctorData["grand-oak"],
      ...doctorData["pine-valley"],
      ...doctorData["willow-gardens"],
    ];
    setDoctors(allDoctors);
  };

  const openPopup = (doctor) => {
    setSelectedDoctor(doctor);
    setShowPopup(true);
  };

  const closePopup = () => {
    setSelectedDoctor(null);
    setShowPopup(false);
  };

  const submitForm = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const patientDetails = {
      name: formData.get("name"),
      ssn: formData.get("ssn"),
      dob: formData.get("dob"),
      address: formData.get("address"),
      phone: formData.get("phone"),
      email: formData.get("email"),
    };

    const payload = {
      hospital: selectedDoctor?.hospital,
      doctor: selectedDoctor?.name,
      patient: patientDetails,
    };

    try {
      const response = await fetch(
        `http://localhost:8000/kong-gateway/${selectedDoctor?.category}/reserve`,
        {
          method: "POST",
          credentials: "include",
          body: JSON.stringify(payload),
        }
      );

      const textResponse = await response.text();
      console.log("Raw Response:", textResponse);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.statusText}`);
      }

      const responseData = JSON.parse(textResponse);

      if (!responseData) {
        throw new Error("Invalid JSON response");
      }

      setReservationStatus({
        success: true,
        hospitalStatuses: responseData,
      });
    } catch (error) {
      console.error("Error during API call:", error);

      setReservationStatus({
        success: false,
        message: `Error booking appointment: ${error.message}`,
      });
    }
  };

  useState(() => {
    fetchDoctors();
  }, []);

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Healthcare App</h1>

        <ul>
          {doctors.map((doctor, index) => (
            <li
              key={index}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "16px",
              }}
            >
              <strong>{doctor.name}</strong> | {doctor.category} |{" "}
              {doctor.availability} | ${doctor.price}{" "}
              <div className={styles.ctas} style={{ marginLeft: "16px" }}>
                <a
                  className={styles.primary}
                  onClick={() => openPopup(doctor)}
                  role="button"
                  tabIndex={0}
                >
                  Book Appointment
                </a>
              </div>
            </li>
          ))}
        </ul>

        {showPopup && (
          <div className={styles.popup}>
            <div className={styles.popupContent}>
              <h3>Book Appointment with {selectedDoctor?.name}</h3>
              <form onSubmit={submitForm}>
                <div className={styles.popupActions}>
                  <label htmlFor="name">Name:</label>
                  <input type="text" name="name" id="name" required />
                </div>

                <div className={styles.popupActions}>
                  <label htmlFor="dob">DOB:</label>
                  <input type="date" name="dob" id="dob" required />
                </div>

                <div className={styles.popupActions}>
                  <label htmlFor="address">Address:</label>
                  <input type="text" name="address" id="address" required />
                </div>

                <div className={styles.popupActions}>
                  <label htmlFor="phone">Phone:</label>
                  <input type="text" name="phone" id="phone" required />
                </div>

                <div className={styles.popupActions}>
                  <label htmlFor="email">Email:</label>
                  <input type="email" name="email" id="email" required />
                </div>

                <div className={styles.popupActions}>
                  <label htmlFor="ssn">SSN:</label>
                  <input type="text" name="ssn" id="ssn" required />
                </div>

                <div className={styles.popupActions}>
                  <button
                    type="button"
                    className={styles.primary}
                    onClick={closePopup}
                  >
                    Cancel
                  </button>
                  <button type="submit" className={styles.primary}>
                    Submit
                  </button>
                </div>
              </form>

              {reservationStatus && reservationStatus.hospitalStatuses && (
                <div style={{ marginTop: "16px" }}>
                  {Object.keys(reservationStatus.hospitalStatuses).map(
                    (hospital) => {
                      const status =
                        reservationStatus.hospitalStatuses[hospital];
                      let message = "";

                      if (status.error) {
                        message = `Error: ${status.error}`;
                      } else if (
                        status.status === "Reserved" ||
                        status.confirmed
                      ) {
                        message = `Reservation successful with Dr. ${
                          status.doctor || selectedDoctor?.name
                        } at ${selectedDoctor?.hospital}. Appointment ID: ${
                          status.appointment_id || status.appointmentNumber
                        }. Fee: $${status.fee}`;
                      } else if (
                        status.detail ||
                        status.status === "Invalid Category"
                      ) {
                        message = `Error: ${status.detail || status.status}`;
                      }

                      return (
                        <div key={hospital} style={{ marginBottom: "12px" }}>
                          <strong>
                            {hospital.replace("_", " ").toUpperCase()}:
                          </strong>{" "}
                          {message}
                        </div>
                      );
                    }
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
      <footer className={styles.footer}></footer>
    </div>
  );
}
