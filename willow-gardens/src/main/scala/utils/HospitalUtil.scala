package com.hospital.pinevalley
package utils

import com.hospital.pinevalley.daos.{Appointment, AppointmentRequest, Doctor, HospitalDAO}

import java.util.Calendar

object HospitalUtil {

  private var appointmentNumber: Int = 1

  // Function to create a new appointment
  def makeNewAppointment(appointmentRequest: AppointmentRequest, hospitalDAO: HospitalDAO): Option[Appointment] = {
    val doctor: Doctor = hospitalDAO.findDoctorByName(appointmentRequest.doctor) match {
      case Some(doctor) if doctor.hospital.equalsIgnoreCase(appointmentRequest.hospital) => doctor
      case _ => return None
    }

    val newAppointment = new Appointment()
    newAppointment.appointmentNumber = appointmentNumber
    appointmentNumber += 1
    newAppointment.doctor = doctor
    newAppointment.patient = appointmentRequest.patient
    newAppointment.fee = doctor.fee
    newAppointment.confirmed = false

    Some(newAppointment)
  }

  def checkForDiscounts(dob: String): Int = {
    val yob = dob.split("-")(0).toInt
    val currentYear = Calendar.getInstance.get(Calendar.YEAR)
    val age = currentYear - yob

    if (age < 12) {
      15
    } else if (age > 55) {
      20
    } else {
      0
    }
  }

  def checkDiscountEligibility(dob: String): Boolean = {
    val yob = dob.split("-")(0).toInt
    val currentYear = Calendar.getInstance.get(Calendar.YEAR)
    val age = currentYear - yob

    age < 12 || age > 55
  }
}

