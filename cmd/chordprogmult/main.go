package main

import (
	"cmp"
	"flag"
	"log/slog"
	"net/http"
	"os"
	"time"

	"github.com/warpyn/chord-prog-mult/internal/catalog"
	"github.com/warpyn/chord-prog-mult/internal/web"
)

func main() {
	healthcheck := flag.Bool("healthcheck", false, "exit 0 if the server on PORT answers GET / with 200, else exit 1")
	flag.Parse()

	port := cmp.Or(os.Getenv("PORT"), "8080")
	if *healthcheck {
		os.Exit(checkHealth(port))
	}

	songs, err := catalog.Load()
	if err != nil {
		slog.Error("load catalog", "error", err)
		os.Exit(1)
	}
	slog.Info("loaded catalog", "songs", len(songs))

	server := &http.Server{
		Addr:              ":" + port,
		Handler:           web.Routes(web.NewHandlers(songs)),
		ReadHeaderTimeout: 5 * time.Second,
	}
	slog.Info("listening", "addr", server.Addr)
	if err := server.ListenAndServe(); err != nil {
		slog.Error("server stopped", "error", err)
		os.Exit(1)
	}
}

func checkHealth(port string) int {
	client := http.Client{Timeout: 2 * time.Second}
	resp, err := client.Get("http://127.0.0.1:" + port + "/")
	if err != nil {
		return 1
	}
	resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 1
	}
	return 0
}
