FROM openjdk:17-jdk-slim AS builder

ARG SBT_VERSION=1.10.5

RUN apt-get update && \
    apt-get install -y curl && \
    mkdir /working/ && \
    cd /working/ && \
    curl -L -o sbt-$SBT_VERSION.deb https://repo.scala-sbt.org/scalasbt/debian/sbt-$SBT_VERSION.deb && \
    dpkg -i sbt-$SBT_VERSION.deb && \
    rm sbt-$SBT_VERSION.deb && \
    apt-get update && \
    apt-get install -y sbt && \
    cd && \
    rm -r /working/

WORKDIR /app

COPY build.sbt . 
COPY project ./project/

RUN sbt update

COPY . .

RUN sbt clean compile assembly

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY --from=builder /app/target/scala-3.3.4/PineValleyService-assembly.jar /app/app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
