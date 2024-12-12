package com.hospital.pinevalley

import daos.{Appointment, AppointmentRequest, ChannelingFeeDao, Doctor, HospitalDAO, Patient, PatientDetails, PatientRecord, Status}
import utils.HospitalUtil

import akka.http.scaladsl.model.ContentTypes.`application/json`
import akka.http.scaladsl.model.{HttpEntity, HttpResponse, StatusCode, StatusCodes}
import com.fasterxml.jackson.databind.json.JsonMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer
import scala.concurrent.Future



class HospitalService {

  private val appointments = mutable.HashMap[Int, Appointment]()
  private val hospitalDAO = HospitalDAO()
  private var categories = hospitalDAO.catergories
  categories ++= Seq("surgery", "cardiology", "gynaecology", "ent", "paediatric")
  val doctorsList:  ArrayBuffer[Doctor] = hospitalDAO.doctorsList

  private val mapper = JsonMapper.builder()
    .addModule(DefaultScalaModule)
    .build()

  private def jsonResponse[T](statusCode: StatusCode, data: T): HttpResponse = {
    val jsonData = mapper.writeValueAsString(data)
    HttpResponse(statusCode, entity = HttpEntity(`application/json`, jsonData))
  }

  def reserveAppointment(appointmentRequest: AppointmentRequest, category: String): Future[HttpResponse] = {
    if (hospitalDAO.catergories.contains(category)) {
      val appointment = HospitalUtil.makeNewAppointment(appointmentRequest, hospitalDAO)

      appointment match {
        case Some(app) =>
          appointments += (app.appointmentNumber -> app)
          hospitalDAO.patientMap.put(appointmentRequest.patient.ssn, appointmentRequest.patient)
          if (!hospitalDAO.patientRecordMap.contains(appointmentRequest.patient.ssn)) {
            hospitalDAO.patientRecordMap.put(appointmentRequest.patient.ssn, PatientRecord(appointmentRequest.patient))
          }

          Future.successful(jsonResponse(StatusCodes.OK, app))
        case None =>
          Future.successful(jsonResponse(StatusCodes.BadRequest, Status(s"Doctor ${appointmentRequest.doctor} is not available")))
      }
    } else {
      Future.successful(jsonResponse(StatusCodes.BadRequest, Status("Invalid Category")))
    }
  }

  def checkChannellingFee(id: Int): Future[HttpResponse] = {
    appointments.get(id) match {
      case Some(appointment) =>
        val channelingFee = ChannelingFeeDao(appointment.doctor.fee.toString, appointment.doctor.name.toLowerCase, appointment.patient.name.toLowerCase)
        Future.successful(jsonResponse(StatusCodes.OK, channelingFee))
      case None =>
        Future.successful(jsonResponse(StatusCodes.NotFound, Status("Error. Could not Find the Requested appointment ID")))
    }
  }

  def updatePatientRecord(patientDetails: PatientDetails): Future[HttpResponse] = {
    val SSN = patientDetails.SSN
    val symptoms = patientDetails.symptoms
    val treatments = patientDetails.treatments

    hospitalDAO.patientMap.get(SSN) match {
      case Some(patient) =>
        hospitalDAO.patientRecordMap.get(SSN) match {
          case Some(patientRecord) =>
            patientRecord.updateSymptoms(symptoms)
            patientRecord.updateTreatments(treatments)
            Future.successful(jsonResponse(StatusCodes.OK, Status("Record Update Success")))
          case None =>
            Future.successful(jsonResponse(StatusCodes.NotFound, Status("Could not find valid Patient Record")))
        }
      case None =>
        Future.successful(jsonResponse(StatusCodes.NotFound, Status("Could not find valid Patient Entry")))
    }
  }

  def getPatientRecord(SSN: String): Future[HttpResponse] = {
    hospitalDAO.patientRecordMap.get(SSN) match {
      case Some(patientRecord) => Future.successful(jsonResponse(StatusCodes.OK, patientRecord))
      case None => Future.successful(jsonResponse(StatusCodes.NotFound, Status("Could not find valid Patient Entry")))
    }
  }

  def isEligibleForDiscount(id: Int): Future[HttpResponse] = {
    appointments.get(id) match {
      case Some(appointment) =>
        val eligible = HospitalUtil.checkDiscountEligibility(appointment.patient.dob)
        Future.successful(jsonResponse(StatusCodes.OK, Status(s"$eligible")))
      case None =>
        Future.successful(jsonResponse(StatusCodes.NotFound, Status("Invalid appointment ID")))
    }
  }

  def addNewDoctor(doctor: Doctor): Future[HttpResponse] = {
    if (!categories.contains(doctor.category)) {
      categories = categories :+ doctor.category
    }
    hospitalDAO.findDoctorByName(doctor.name) match {
      case Some(doctor) =>
        doctorsList :+ doctor
        Future.successful(jsonResponse(StatusCodes.OK, Status("New Doctor Added Successfully")))
      case None =>
        Future.successful(jsonResponse(StatusCodes.BadRequest, Status("Doctor Already Exist in the system")))
    }
  }
}
