FROM golang:1.22

WORKDIR /app

RUN go install github.com/codegangsta/gin@latest

COPY go.mod go.sum ./

RUN go mod tidy

COPY . .

EXPOSE 8080

CMD ["gin", "--port", "8080", "--appPort", "8083", "run", "main.go"]
