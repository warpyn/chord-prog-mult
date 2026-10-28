package web

import (
	"net/http"

	"github.com/warpyn/chord-prog-mult/assets"
)

func Routes(h *Handlers) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /{$}", h.Home)
	mux.HandleFunc("GET /catalog", h.Catalog)
	mux.HandleFunc("GET /approach", h.Approach)
	mux.HandleFunc("POST /multiply", h.Multiply)
	mux.HandleFunc("POST /catalog-multiply", h.CatalogMultiply)
	mux.Handle("GET /assets/", http.StripPrefix("/assets/", cacheStatic(http.FileServerFS(assets.FS))))
	mux.HandleFunc("/", h.NotFound)
	return logRequests(recoverPanics(mux))
}
