package com.hospital.pinevalley

import akka.http.scaladsl.server.Route
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport.*
import daos.*

import akka.http.scaladsl.server.Directives._
import com.fasterxml.jackson.databind.json.JsonMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule

class HospitalRoutes(hospitalService: HospitalService) {
  private val mapper = JsonMapper.builder()
    .addModule(DefaultScalaModule)
    .build()

  def route: Route = {
    pathPrefix("api" / "v1" / "categories") {
      pathEndOrSingleSlash {
        get {
          complete("Welcome to the categories API!")
        }
      } ~
      path(Segment / "reserve") { category =>
        post {
          entity(as[String]) { data =>
            val appointmentRequest = mapper.readValue(data, classOf[AppointmentRequest])
            complete(hospitalService.reserveAppointment(appointmentRequest, category))
          }
        }
      } ~
          path("appointments" / IntNumber / "fee") { id =>
          get {
            complete(hospitalService.checkChannellingFee(id))
          }
        } ~
        path("patient" / "updaterecord") {
          post {
            entity(as[String]) { data =>
              val patientDetails = mapper.readValue(data, classOf[PatientDetails])
              complete(hospitalService.updatePatientRecord(patientDetails))
            }
          }
        } ~
        path("patient" / Segment / "getrecord") { SSN =>
          get {
            complete(hospitalService.getPatientRecord(SSN))
          }
        } ~
        path("patient" / "appointment" / IntNumber / "discount") { id =>
          get {
            complete(hospitalService.isEligibleForDiscount(id))
          }
        } ~
        path("admin" / "doctor" / "newdoctor") {
          post {
            entity(as[String]) { data =>
              val doctor = mapper.readValue(data, classOf[Doctor])
              complete(hospitalService.addNewDoctor(doctor))
            }
          }
        }
    }
  }
}
