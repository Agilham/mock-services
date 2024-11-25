package com.hospital.pinevalley
package daos

case class AppointmentRequest (
  patient: Patient,
  doctor: String,
  hospital: String
)