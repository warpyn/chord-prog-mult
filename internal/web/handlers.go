package web

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/a-h/templ"

	"github.com/warpyn/chord-prog-mult/internal/catalog"
	"github.com/warpyn/chord-prog-mult/internal/logic"
	"github.com/warpyn/chord-prog-mult/templates"
)

const (
	lessThanTwoSelected = "Error: Less Than 2 Progressions Selected"
	moreThanTwoSelected = "Error: More Than 2 Progressions Selected"
	selectExactlyTwo    = "Select exactly two progressions to multiply."
)

type Handlers struct {
	songs []catalog.Song
}

func NewHandlers(songs []catalog.Song) *Handlers {
	return &Handlers{songs: songs}
}

func (h *Handlers) Home(w http.ResponseWriter, r *http.Request) {
	render(w, r, templates.Home())
}

func (h *Handlers) Catalog(w http.ResponseWriter, r *http.Request) {
	render(w, r, templates.Catalog(h.songs))
}

func (h *Handlers) Approach(w http.ResponseWriter, r *http.Request) {
	render(w, r, templates.Approach())
}

func (h *Handlers) NotFound(w http.ResponseWriter, r *http.Request) {
	templ.Handler(templates.NotFound(), templ.WithStatus(http.StatusNotFound)).ServeHTTP(w, r)
}

func (h *Handlers) Multiply(w http.ResponseWriter, r *http.Request) {
	progF := r.FormValue("prog_f")
	progG := r.FormValue("prog_g")
	if progF == "" || progG == "" {
		w.WriteHeader(http.StatusNoContent)
		return
	}

	productFG := logic.ChordProgMult(progF, progG)
	productGF := logic.ChordProgMult(progG, progF)
	render(w, r, templates.Result(progF, progG, productFG, productGF))
}

func (h *Handlers) CatalogMultiply(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	column := catalog.Column(r.Form.Get("column"))
	if column != catalog.Symbols && column != catalog.Roman {
		http.Error(w, fmt.Sprintf("invalid column %q", column), http.StatusBadRequest)
		return
	}

	selected, err := h.selectedSongs(r.Form["selected"])
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	switch len(selected) {
	case 0:
		w.WriteHeader(http.StatusNoContent)
	case 1:
		render(w, r, templates.CatalogResult(lessThanTwoSelected, selectExactlyTwo))
	case 2:
		progF := selected[0].Chords(column)
		progG := selected[1].Chords(column)
		lineFG := fmt.Sprintf("(%s)(%s) = %s", progF, progG, logic.ChordProgMult(progF, progG))
		lineGF := fmt.Sprintf("(%s)(%s) = %s", progG, progF, logic.ChordProgMult(progG, progF))
		render(w, r, templates.CatalogResult(lineFG, lineGF))
	default:
		render(w, r, templates.CatalogResult(moreThanTwoSelected, selectExactlyTwo))
	}
}

func (h *Handlers) selectedSongs(indices []string) ([]catalog.Song, error) {
	songs := make([]catalog.Song, 0, len(indices))
	for _, index := range indices {
		i, err := strconv.Atoi(index)
		if err != nil || i < 0 || i >= len(h.songs) {
			return nil, fmt.Errorf("invalid song index %q", index)
		}
		songs = append(songs, h.songs[i])
	}
	return songs, nil
}

func render(w http.ResponseWriter, r *http.Request, component templ.Component) {
	templ.Handler(component).ServeHTTP(w, r)
}
