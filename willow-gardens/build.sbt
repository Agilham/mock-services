ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "3.3.4"

lazy val root = (project in file("."))
  .settings(
    name := "PineValleyService",
    idePackagePrefix := Some("com.hospital.pinevalley"),

    // Add Akka HTTP and json4s dependencies
    libraryDependencies ++= Seq(
      "com.typesafe.akka" %% "akka-http" % "10.5.3",      // Akka HTTP for REST API
      "com.typesafe.akka" %% "akka-stream" % "2.8.6",     // Akka Streams for handling streams
      "com.typesafe.akka" %% "akka-actor-typed" % "2.8.6",      // Akka Actors for the ActorSystem
      "com.typesafe.akka" %% "akka-http-spray-json" % "10.5.3",
      "com.fasterxml.jackson.module" %% "jackson-module-scala" % "2.17.2",
      "ch.qos.logback" % "logback-classic" % "1.5.6"

)
  )
