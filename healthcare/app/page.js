"use client"

import { useState } from "react";
import styles from "./page.module.css";

export default function Home() {
  const [doctors, setDoctors] = useState([]);

  const fetchDoctors = (hospital) => {
    fetch(`http://localhost:8000/${hospital}/doctors`)
      .then((response) => response.json())
      .then((data) => setDoctors(data))
      .catch((error) => console.error("Error fetching doctors:", error));
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1>Healthcare Service</h1>
        <h2>Available Doctors</h2>
        <div className={styles.ctas}>
          <button
            className={styles.primary}
            onClick={() => fetchDoctors("pine-valley")}
          >
            Pine Valley Hospital
          </button>
          <button
            className={styles.secondary}
            onClick={() => fetchDoctors("grand-oak")}
          >
            Grand Oak Hospital
          </button>
        </div>
        <ul className={styles.list}>
          {doctors.map((doctor, index) => (
            <li key={index} className={styles.listItem}>
              <strong>{doctor.name}</strong> ({doctor.category}) -{" "}
              {doctor.schedule} - ${doctor.fee}
            </li>
          ))}
        </ul>
      </main>
      <footer className={styles.footer}>
        <a
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by Next.js
        </a>
      </footer>
    </div>
  );
}
