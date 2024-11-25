package com.hospital.pinevalley
package daos

class Appointment(
  var time: String = null,
  var appointmentNumber : Int = 0,
  var doctor: Doctor = null,
  var patient: Patient = null,
  var hospital: String = null,
  var fee : Double = .0,
  var confirmed : Boolean = false,
  var paymentID: String = null
)

