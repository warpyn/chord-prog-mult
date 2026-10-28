FROM golang:1.27-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/chordprogmult ./cmd/chordprogmult

FROM gcr.io/distroless/static:nonroot
COPY --from=builder /out/chordprogmult /chordprogmult
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD ["/chordprogmult", "-healthcheck"]
ENTRYPOINT ["/chordprogmult"]
