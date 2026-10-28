package web

import (
	"bytes"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"

	"github.com/warpyn/chord-prog-mult/internal/catalog"
)

func serve(t *testing.T, method, target string, form url.Values) *httptest.ResponseRecorder {
	t.Helper()

	songs, err := catalog.Load()
	if err != nil {
		t.Fatal(err)
	}

	req := httptest.NewRequest(method, target, strings.NewReader(form.Encode()))
	if form != nil {
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	}
	rec := httptest.NewRecorder()
	Routes(NewHandlers(songs)).ServeHTTP(rec, req)
	return rec
}

func assertResponse(t *testing.T, rec *httptest.ResponseRecorder, wantStatus int, wantBody ...string) {
	t.Helper()

	if rec.Code != wantStatus {
		t.Errorf("status = %d, want %d", rec.Code, wantStatus)
	}
	for _, want := range wantBody {
		if !strings.Contains(rec.Body.String(), want) {
			t.Errorf("body does not contain %q:\n%s", want, rec.Body.String())
		}
	}
	if wantStatus == http.StatusNoContent && rec.Body.Len() != 0 {
		t.Errorf("204 response has body %q", rec.Body.String())
	}
}

func TestPages(t *testing.T) {
	tests := []struct {
		path       string
		wantStatus int
		wantBody   []string
	}{
		{"/", http.StatusOK, []string{`hx-post="/multiply"`, `name="prog_f"`, `name="prog_g"`, `id="result"`}},
		{"/catalog", http.StatusOK, []string{`hx-post="/catalog-multiply"`, `id="catalog-data"`, "We Never Change", `id="catalog-result"`, "/assets/js/catalog.js"}},
		{"/approach", http.StatusOK, []string{"What is a Chord Progression?", "Multiplying Cycles"}},
		{"/nope", http.StatusNotFound, []string{"Error 404. Page Not Found."}},
		{"/catalog/nope", http.StatusNotFound, []string{"Error 404. Page Not Found."}},
	}
	layoutBody := []string{
		"<title>Chord Progression Multiplication</title>",
		`content="width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5"`,
		"/assets/css/bootstrap.css",
		"/assets/css/styles.css",
		"/assets/js/htmx.min.js",
		"/chord-prog-mult",
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			rec := serve(t, http.MethodGet, tt.path, nil)
			assertResponse(t, rec, tt.wantStatus, append(layoutBody, tt.wantBody...)...)
			if got := rec.Header().Get("Content-Type"); got != "text/html; charset=utf-8" {
				t.Errorf("Content-Type = %q, want text/html", got)
			}
		})
	}
}

func TestAssets(t *testing.T) {
	tests := []struct {
		path            string
		wantContentType string
	}{
		{"/assets/css/bootstrap.css", "text/css; charset=utf-8"},
		{"/assets/js/htmx.min.js", "text/javascript; charset=utf-8"},
		{"/assets/js/alpine.min.js", "text/javascript; charset=utf-8"},
		{"/assets/css/styles.css", "text/css; charset=utf-8"},
		{"/assets/js/catalog.js", "text/javascript; charset=utf-8"},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			rec := serve(t, http.MethodGet, tt.path, nil)
			assertResponse(t, rec, http.StatusOK)
			if got := rec.Header().Get("Content-Type"); got != tt.wantContentType {
				t.Errorf("Content-Type = %q, want %q", got, tt.wantContentType)
			}
			if got := rec.Header().Get("Cache-Control"); got != "public, max-age=3600" {
				t.Errorf("Cache-Control = %q, want public, max-age=3600", got)
			}
		})
	}
}

func TestMultiply(t *testing.T) {
	tests := []struct {
		name       string
		progF      string
		progG      string
		wantStatus int
		wantBody   []string
	}{
		{"both empty", "", "", http.StatusNoContent, nil},
		{"f empty", "", "C G", http.StatusNoContent, nil},
		{"g empty", "C G", "", http.StatusNoContent, nil},
		{"space is not empty", " ", "C", http.StatusOK, []string{`<div id="result">`}},
		{"both orders", "C G", "F Bb C", http.StatusOK, []string{
			"(f)(g) = (C G)(F Bb C) = (F Bb G C)",
			"(g)(f) = (F Bb C)(C G) = (C G F Bb)",
		}},
		{"duplicate chords", "C C", "G", http.StatusOK, []string{
			"(f)(g) = (C C)(G) = Invalid Input: Duplicate Chords Found",
		}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			form := url.Values{"prog_f": {tt.progF}, "prog_g": {tt.progG}}
			rec := serve(t, http.MethodPost, "/multiply", form)
			assertResponse(t, rec, tt.wantStatus, tt.wantBody...)
		})
	}
}

func TestCatalogMultiply(t *testing.T) {
	tests := []struct {
		name       string
		column     string
		selected   []string
		wantStatus int
		wantBody   []string
	}{
		{"none selected", "symbols", nil, http.StatusNoContent, nil},
		{"one selected", "symbols", []string{"0"}, http.StatusOK, []string{lessThanTwoSelected, selectExactlyTwo}},
		{"three selected", "symbols", []string{"0", "1", "2"}, http.StatusOK, []string{moreThanTwoSelected, selectExactlyTwo}},
		{"two symbols in click order", "symbols", []string{"1", "0"}, http.StatusOK, []string{
			"(Bm F#m E)(F#m E) = (F#m Bm)(E)",
			"(F#m E)(Bm F#m E) = (Bm E)(F#m)",
		}},
		{"two roman", "roman", []string{"0", "1"}, http.StatusOK, []string{
			"(vi V)(ii vi V) = (ii V)(vi)",
			"(ii vi V)(vi V) = (vi ii)(V)",
		}},
		{"index past end", "symbols", []string{"0", "34"}, http.StatusBadRequest, nil},
		{"negative index", "symbols", []string{"-1", "0"}, http.StatusBadRequest, nil},
		{"non-numeric index", "symbols", []string{"x", "0"}, http.StatusBadRequest, nil},
		{"unknown column", "letters", []string{"0", "1"}, http.StatusBadRequest, nil},
		{"missing column", "", []string{"0", "1"}, http.StatusBadRequest, nil},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			form := url.Values{"column": {tt.column}, "selected": tt.selected}
			rec := serve(t, http.MethodPost, "/catalog-multiply", form)
			assertResponse(t, rec, tt.wantStatus, tt.wantBody...)
		})
	}
}

func TestRecoverPanics(t *testing.T) {
	var logs bytes.Buffer
	defaultLogger := slog.Default()
	slog.SetDefault(slog.New(slog.NewTextHandler(&logs, nil)))
	t.Cleanup(func() { slog.SetDefault(defaultLogger) })

	mux := http.NewServeMux()
	mux.HandleFunc("GET /panic", func(http.ResponseWriter, *http.Request) { panic("boom") })
	mux.HandleFunc("GET /ok", func(http.ResponseWriter, *http.Request) {})
	server := httptest.NewServer(logRequests(recoverPanics(mux)))
	defer server.Close()

	for _, tt := range []struct {
		path       string
		wantStatus int
	}{
		{"/panic", http.StatusInternalServerError},
		{"/ok", http.StatusOK},
	} {
		res, err := http.Get(server.URL + tt.path)
		if err != nil {
			t.Fatal(err)
		}
		res.Body.Close()
		if res.StatusCode != tt.wantStatus {
			t.Errorf("GET %s status = %d, want %d", tt.path, res.StatusCode, tt.wantStatus)
		}
	}

	for _, want := range []string{"msg=panic", "panic=boom", "stack=", "path=/panic status=500 duration=", "path=/ok status=200 duration="} {
		if !strings.Contains(logs.String(), want) {
			t.Errorf("logs do not contain %q:\n%s", want, logs.String())
		}
	}
}
