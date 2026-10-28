# Chord Progression Multiplication

https://chord-prog-mult.herokuapp.com/

Chord progressions are sequences of chords that express harmony in music, and this idea is the cornerstone of Western tonal music. The goal of this project is to use abstract algebra, specifically the symmetric group's multiplication operation, to manipulate chord progressions as well as explore connections between math and music.

This website provides a calculator to multiply custom chord progressions and an interactive catalog on the Catalog page to multiply chord progressions found in music. To read more about the mathematical reasoning behind the multiplication idea, visit the Approach page.

The website was written in Python using the Dash open source framework by Plotly. All the python package dependencies for this project are listed in the requirements.txt file. Notable Python libraries used include NumPy and Pandas.

## Development (Go)

The Go version needs Go 1.27 or later. templ is a `go.mod` tool, so `go tool templ` runs it and no global install is necessary.

- `make run` generates the templates and starts the server at http://localhost:8080. Set `PORT` to use a different port.
- `make dev` watches the `.templ` and `.go` files, regenerates the templates, restarts the server, and reloads the browser. Open the templ proxy at **http://localhost:7331**, not port 8080, because only the proxy reloads the browser.
- `make test` runs all tests.
- `make generate` writes the `*_templ.go` files. Run it before each commit, because watch mode does not always rewrite them. `make check-generated` fails if the committed files are stale.
- The files in `assets/` are embedded in the binary. After a CSS or JS edit in `make dev`, save any `.go` file to restart the server.
