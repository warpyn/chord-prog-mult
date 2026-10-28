package catalog

import (
	_ "embed"
	"encoding/csv"
	"fmt"
	"slices"
	"strings"
)

//go:embed prog_catalog.csv
var catalogCSV string

var expectedHeader = []string{"Song", "Artist", "Section", "Progression", "Roman Numerals"}

type Column string

const (
	Symbols Column = "symbols"
	Roman   Column = "roman"
)

type Song struct {
	Song          string
	Artist        string
	Section       string
	Progression   string
	RomanNumerals string
}

func (s Song) Chords(c Column) string {
	if c == Roman {
		return s.RomanNumerals
	}
	return s.Progression
}

func Load() ([]Song, error) {
	r := csv.NewReader(strings.NewReader(strings.TrimPrefix(catalogCSV, "\uFEFF")))
	r.FieldsPerRecord = len(expectedHeader)
	rows, err := r.ReadAll()
	if err != nil {
		return nil, err
	}
	if len(rows) == 0 || !slices.Equal(rows[0], expectedHeader) {
		return nil, fmt.Errorf("catalog: unexpected header %q", rows[:min(len(rows), 1)])
	}

	songs := make([]Song, 0, len(rows)-1)
	for _, row := range rows[1:] {
		songs = append(songs, Song{
			Song:          row[0],
			Artist:        row[1],
			Section:       row[2],
			Progression:   row[3],
			RomanNumerals: row[4],
		})
	}
	return songs, nil
}
