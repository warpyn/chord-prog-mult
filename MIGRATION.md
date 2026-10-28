# Migration from Python/Dash to Go

The site was a Python app built with Dash, pandas, and NumPy, deployed on Heroku. It is now a Go server with templ, HTMX, and Alpine.js in a distroless container. The visible behavior is the same, except for the changes listed in [Intentional changes](#intentional-changes).

The last Python version is the git tag `python-final`.

## What changed and why

- **No database.** The Python app read the catalog CSV with pandas. The Go app embeds the same CSV in the binary and loads its 34 read-only rows into memory at startup. SQLite was considered for the port and rejected: it adds a schema and a CGO dependency, and the static build uses `CGO_ENABLED=0`.
- **No NumPy or pandas.** The algorithm composes two small permutations. Plain `[]int` slices do the same work.
- **templ instead of Dash layouts.** Pages are type-checked Go components. The generated `*_templ.go` files are committed, so a build or a Docker image does not need templ.
- **HTMX instead of Dash callbacks.** The Multiply buttons send a form to `POST /multiply` or `POST /catalog-multiply`, and the server returns an HTML fragment. A `204 No Content` response leaves the old output on the page, as Dash `PreventUpdate` did.
- **Alpine.js for client state.** The catalog search, sort, column toggle, selection order, and the mobile navbar run in Alpine. There is no Bootstrap JS.
- **Standard library routing.** `net/http` `ServeMux` with method patterns. There is no web framework.
- **Embedded assets.** CSS and JS are vendored in `assets/` and embedded with `//go:embed`. HTMX, Alpine, and the Bootswatch theme are not loaded from a CDN.
- **Distroless container.** A two-stage build gives a static binary on `gcr.io/distroless/static:nonroot` (about 10MB). The binary has a `-healthcheck` flag, because the image has no shell or `curl`.

## Behavior parity rules

These rules come from the Python source. They are the checklist for a change to the algorithm or the handlers.

### Algorithm

1. Split input with `strings.Split(s, " ")`, never `strings.Fields`. Python `split(' ')` keeps empty tokens, and an empty token is a real chord. `"C  G"` has three chords, and the catalog row *We Never Change / Chorus* has a trailing space.
2. Do not trim input.
3. Check `prog1` for duplicates first, then `prog2`. Both return `Invalid Input: Duplicate Chords Found`.
4. The "No Progression Detected" check is ported, but no input can reach it (`"".split(' ')` is `[""]`).
5. Number the chords of `prog1` first, in order of first appearance, then the new chords of `prog2`. Each cycle starts at the lowest unused number. This order sets the output.
6. The call is `ChordProgMult(prog2, prog1)`: right-to-left composition, `prog1` first.
7. Print fixed points as one-chord cycles, for example `(F)`.
8. Format: `(a b c)` with single spaces in a cycle and nothing between cycles, for example `(C F)(G)`.

### Home page

9. If a field is empty, the server returns `204`, and the old output stays.
10. A field that contains only spaces is not empty.
11. Output: `(f)(g) = (<f>)(<g>) = <fg>` and `(g)(f) = (<g>)(<f>) = <gf>`.

### Catalog page

12. The table always shows all five columns. The radio toggle selects the column to multiply and the column in the "Selected Progressions" table.
13. The "Selected Progressions" table updates when the selection changes.
14. Output has no `(f)(g) = ` prefix: `(<f>)(<g>) = <fg>` and `(<g>)(<f>) = <gf>`.
15. Selection count: 0 gives `204`; 1 gives `Error: Less Than 2 Progressions Selected`; more than 2 gives `Error: More Than 2 Progressions Selected`; 2 gives both products.
16. f and g are in click order, the same as Dash `selected_rows`. This was checked against the Python app.
17. A selected row that the search hides stays selected.

### Shell

18. Title `Chord Progression Multiplication`. Viewport `width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5`.
19. An unknown path shows `Error 404. Page Not Found.`

### Intentional changes

- No pagination. Dash showed 11 catalog rows per page; all 34 rows now show on one page.
- One search box instead of a filter for each column.
- An unknown path returns status `404`. Dash returned `200`.
- Enter in a calculator input runs Multiply. Enter in the catalog search box does nothing.
- The calculator labels are `<label for=...>` elements.
- The mobile navbar opens and closes with no animation.
- A click on a catalog header sorts by that column and shows `↕`, `▲`, or `▼`.

## Golden tests

`internal/logic/testdata/golden.json` holds 2,568 cases from the Python algorithm:

- All ordered pairs in each catalog column: 34 × 34 chord symbols and 34 × 34 Roman numerals.
- All ordered pairs of 16 edge inputs: double, leading, and trailing spaces, only a space, an empty string, one chord, duplicates, and fixed points.

`TestChordProgMultMatchesPython` runs the Go algorithm on each case and compares the output. The file is committed and is the source of truth now that the Python code is gone.

To make the file again, use a checkout of the `python-final` tag. NumPy is the only dependency.

```bash
git worktree add ../chord-prog-mult-python python-final
python3 -m venv ../chord-prog-mult-python/.venv
../chord-prog-mult-python/.venv/bin/pip install numpy
../chord-prog-mult-python/.venv/bin/python scripts/gen_golden.py ../chord-prog-mult-python > internal/logic/testdata/golden.json
```

Before the Python code was removed, the two apps were also compared directly: 327 calculator pairs over HTTP and 10 catalog click sequences in a headless browser. There were no differences.

## Intentionally dropped

Do not add these back without a new reason:

- A database. SQLite was considered for the port and rejected.
- pandas and NumPy.
- Dash, its callbacks, and `dash_table`.
- Catalog pagination and the filter for each column.
- Bootstrap JS.
- `air` and a dev docker-compose file. `make dev` (`templ generate --watch`) already rebuilds, restarts, and reloads.
- Heroku files: `Procfile`, `requirements.txt`, and `runtime.txt`.
