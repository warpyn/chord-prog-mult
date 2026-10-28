# Chord Progression Multiplication

Chord progressions are sequences of chords that express harmony in music, and this idea is the cornerstone of Western tonal music. The goal of this project is to use abstract algebra, specifically the symmetric group's multiplication operation, to manipulate chord progressions as well as explore connections between math and music.

This website provides a calculator to multiply custom chord progressions and an interactive catalog on the Catalog page to multiply chord progressions found in music. To read more about the mathematical reasoning behind the multiplication idea, visit the Approach page.

The Go version is not deployed yet. A link to the site will be added here when the new host is live.

The website is written in Go. The server uses the standard library for routing, [templ](https://templ.guide) for HTML templates, and [HTMX](https://htmx.org) and [Alpine.js](https://alpinejs.dev) for interactivity. The catalog, the templates, and the static assets are embedded in one static binary, with no database. The original version was written in Python with Dash, NumPy, and pandas; see [MIGRATION.md](MIGRATION.md) for what changed.

## Prerequisites

- Go 1.27 or later.
- templ is a `go.mod` tool, so `go tool templ` runs it. No global install is necessary.
- Docker, only for the container image.

## Development

- `make run` generates the templates and starts the server at http://localhost:8080. Set `PORT` to use a different port.
- `make dev` watches the `.templ` and `.go` files, regenerates the templates, restarts the server, and reloads the browser. Open the templ proxy at **http://localhost:7331**, not port 8080, because only the proxy reloads the browser.
- `make test` runs all tests.
- `make build` writes a static binary to `bin/chordprogmult`.
- `make generate` writes the `*_templ.go` files. Run it before each commit, because watch mode does not always rewrite them. `make check-generated` fails if the committed files are stale. CI runs the same check.
- The files in `assets/` are embedded in the binary. After a CSS or JS edit in `make dev`, save any `.go` file to restart the server.

## Docker

```bash
docker build -t chord-prog-mult .
docker run --rm -p 8080:8080 chord-prog-mult
```

`make docker` runs both commands. The image is about 10MB: a static binary on `gcr.io/distroless/static:nonroot`, as a non-root user. The build compiles the committed `*_templ.go` files, so it does not need templ. The image health check runs `/chordprogmult -healthcheck`, which sends `GET /` to the server and exits `0` on a `200` status.

## Project layout

```
cmd/chordprogmult/     main: server setup, PORT, -healthcheck flag
internal/logic/        chord progression multiplication, golden tests
internal/catalog/      embedded prog_catalog.csv and its loader
internal/web/          routes, handlers, middleware
templates/             .templ files and the generated *_templ.go files
assets/                embedded CSS and JS (served at /assets/)
scripts/gen_golden.py  writes internal/logic/testdata/golden.json from the Python app
```

## Vendored front-end files

These files are in `assets/` and are not loaded from a CDN:

| File | Version |
|---|---|
| `js/htmx.min.js` | htmx.org 2.0.11 |
| `js/alpine.min.js` | alpinejs 3.17.4 (`dist/cdn.min.js`) |
| `css/bootstrap.css` | Bootswatch Litera 4.5.3 (Bootstrap 4) |

To upgrade one, replace the file and run the app to check the pages.

## Add a catalog entry

1. Add a row to `internal/catalog/prog_catalog.csv` with the columns `Song,Artist,Section,Progression,Roman Numerals`. Separate the chords with single spaces.
2. Update the row count in `internal/catalog/catalog_test.go` and the "index past end" case in `internal/web/handlers_test.go`.
3. Run `make test`, and then rebuild or restart the server. The CSV is embedded, so a running server does not see the change.
