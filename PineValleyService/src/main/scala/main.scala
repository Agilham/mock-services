package com.hospital.pinevalley

import daos.{Doctor, Patient}

import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import com.typesafe.config.{Config, ConfigFactory}
import akka.http.scaladsl.server.Directives.*
import akka.http.scaladsl.server.Route

import scala.concurrent.ExecutionContextExecutor
import scala.io.StdIn

object main {

  def main(args: Array[String]): Unit = {

    implicit val system: ActorSystem[Any] = ActorSystem(Behaviors.empty, "my-system")
    implicit val executionContext: ExecutionContextExecutor = system.executionContext

    val config : Config = ConfigFactory.load()

    val hospitalService = new HospitalService()
    hospitalService.doctorsList.addOne(Doctor("seth mears", "pine valley community hospital", "surgery", "3.00 p.m - 5.00 p.m", 8000))
    hospitalService.doctorsList.addOne(Doctor("emeline fulton", "pine valley community hospital", "cardiology", "8.00 a.m - 10.00 a.m", 4000))
    val hospitalRoutes = new HospitalRoutes(hospitalService)

    val routes: Route = pathPrefix("api") {
      path("test") {
        get {
          complete("This is a test route.")
        }
      }
    }

    println(system.settings.config.getString("akka.http.server.log-unmatched-routes"))
    val port = config.getInt("server.port")
    val bindingFuture = Http().newServerAt("localhost", port).bind(routes ~ hospitalRoutes.route)
  }
}