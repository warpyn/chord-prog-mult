package main

import (
	"log"
	"net/http"
)

func main() {
	server := &http.Server{Addr: ":8080"}
	log.Fatal(server.ListenAndServe())
}
