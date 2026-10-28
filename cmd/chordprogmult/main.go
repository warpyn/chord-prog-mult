package main

import (
	"log"
	"net/http"

	"github.com/warpyn/chord-prog-mult/internal/catalog"
)

func main() {
	songs, err := catalog.Load()
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("loaded %d catalog songs", len(songs))

	server := &http.Server{Addr: ":8080"}
	log.Fatal(server.ListenAndServe())
}
