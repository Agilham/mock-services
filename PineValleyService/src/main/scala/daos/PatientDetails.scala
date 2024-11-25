package com.hospital.pinevalley
package daos

import scala.collection.mutable.ArrayBuffer

case class PatientDetails(
  SSN: String,
  symptoms: ArrayBuffer[String],
  treatments: ArrayBuffer[String]
)
