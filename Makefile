.PHONY: generate build run dev test check-generated docker

generate:
	go tool templ generate

build: generate
	CGO_ENABLED=0 go build -o bin/chordprogmult ./cmd/chordprogmult

run: generate
	go run ./cmd/chordprogmult

dev:
	go tool templ generate --watch --proxy="http://localhost:8080" --cmd="go run ./cmd/chordprogmult"

test:
	go test ./...

check-generated: generate
	test -z "$$(git status --porcelain -- '*_templ.go')"

docker:
	docker build -t chord-prog-mult . && docker run --rm -p 8080:8080 chord-prog-mult
