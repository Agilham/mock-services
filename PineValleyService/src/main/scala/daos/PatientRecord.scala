package com.hospital.pinevalley
package daos

import java.text.SimpleDateFormat
import java.util.Date
import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

class PatientRecord(private var patient: Patient) {
  private var symptoms = mutable.HashMap[String,ArrayBuffer[String]]()
  private var treatments = mutable.HashMap[String,ArrayBuffer[String]]()

  def updateTreatments(treatments: ArrayBuffer[String]): Unit = {
    val date = new SimpleDateFormat("dd-MM-yyyy").format(new Date())
    this.treatments.put(date, treatments)
  }

  def updateSymptoms(symptoms: ArrayBuffer[String]): Unit = {
    val date = new SimpleDateFormat("dd-MM-yyyy").format(new Date())
    this.symptoms.put(date, symptoms)
  }
}
