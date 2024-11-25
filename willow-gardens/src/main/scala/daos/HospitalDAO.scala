package com.hospital.pinevalley
package daos

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

class HospitalDAO :
    var doctorsList : ArrayBuffer[Doctor] = ArrayBuffer()
    var catergories : ArrayBuffer[String] = ArrayBuffer()
    var patientMap : mutable.HashMap[String, Patient] = mutable.HashMap()
    var patientRecordMap : mutable.HashMap[String, PatientRecord] = mutable.HashMap()
  
    def findDoctorByCategory(category: String): ArrayBuffer[Doctor] = {
      val list = ArrayBuffer[Doctor]()
      for (doctor <- doctorsList) {
        if (category.equals(doctor.category)) list.append(doctor)
      }
      list
    }
  
    def findDoctorByName(name: String): Option[Doctor] = {
      doctorsList.find(doctor => doctor.name == name)
    }
