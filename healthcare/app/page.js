"use client";

import styles from "./page.module.css";
import { useState } from "react";

const doctorData = {
  "grand-oak": [
    {
      name: "Dr. John Doe",
      hospital: "Grand-oak Hospital",
      category: "Cardiology",
      availability: "8.00 - 15.00",
      price: 100000,
    },
    {
      name: "Dr. Jane Doe",
      hospital: "Grand-oak Hospital",
      category: "Tooth",
      availability: "8.00 - 16.00",
      price: 150000,
    },
    {
      name: "Dr. John Smith",
      hospital: "Grand-oak Hospital",
      category: "Child",
      availability: "9.00 - 14.00",
      price: 200000,
    },
  ],
  "pine-valley": [
    {
      name: "seth mears",
      hospital: "pine valley community hospital",
      category: "surgery",
      availability: "3.00 p.m - 5.00 p.m",
      price: 8000,
    },
    {
      name: "emeline Fulton",
      hospital: "pine valley community hospital",
      category: "cardiology",
      availability: "8.00 a.m - 10.00 a.m",
      price: 4000,
    },
  ],
  "willow-gardens": [
    {
      name: "Dr. John Doe",
      hospital: "Willow-gardens Hospital",
      category: "Cardiology",
      availability: "8.00 - 15.00",
      price: 100000,
    },
    {
      name: "Dr. Jane Doe",
      hospital: "Willow-gardens Hospital",
      category: "Tooth",
      availability: "8.00 - 16.00",
      price: 150000,
    },
    {
      name: "Dr. John Smith",
      hospital: "Willow-gardens Hospital",
      category: "Child",
      availability: "9.00 - 14.00",
      price: 200000,
    },
  ],
};

export default function Home() {
  const [doctors, setDoctors] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);

  const fetchDoctors = (hospital) => {
    setDoctors(doctorData[hospital] || []);
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

    let chosenHospital = "";
    if (selectedDoctor?.hospital == "Grand-oak Hospital") {
      chosenHospital = "grand-oak";
    } else if (selectedDoctor?.hospital == "pine valley community hospital") {
      chosenHospital = "pine-valley";
    } else if (selectedDoctor?.hospital == "Willow-gardens Hospital") {
      chosenHospital = "willow-gardens";
    }

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

      if (!response.ok) {
        const errorDetails = await response.json();
        throw new Error(errorDetails.message || "Failed to book appointment");
      }

      alert("Appointment booked successfully!");
      closePopup();
    } catch (error) {
      console.error("Error:", error);
      alert(`Error booking appointment: ${error.message}`);
    }
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Healthcare App</h1>

        <ol>
          <li>Select a hospital to view its available doctors.</li>
          <li>Select a doctor and fill out the form to book an appointment.</li>
        </ol>

        <div className={styles.ctas}>
          <a
            className={styles.secondary}
            onClick={() => fetchDoctors("grand-oak")}
            role="button"
            tabIndex={0}
          >
            Grand Oak Hospital
          </a>
          <a
            className={styles.secondary}
            onClick={() => fetchDoctors("pine-valley")}
            role="button"
            tabIndex={0}
          >
            Pine Valley Hospital
          </a>
          <a
            className={styles.secondary}
            onClick={() => fetchDoctors("willow-gardens")}
            role="button"
            tabIndex={0}
          >
            Willow Gardens Hospital
          </a>
        </div>

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
              <strong>
                {doctor.name} ({doctor.hospital})
              </strong>{" "}
              | {doctor.category} | {doctor.availability} | ${doctor.price}{" "}
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
              <h3>
                Book Appointment with {selectedDoctor?.name} (
                {selectedDoctor?.hospital})
              </h3>
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
                  <button type="submit" className={styles.primary}>
                    Submit
                  </button>
                  <button
                    type="button"
                    className={styles.primary}
                    onClick={closePopup}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
      <footer className={styles.footer}></footer>
    </div>
  );
}
