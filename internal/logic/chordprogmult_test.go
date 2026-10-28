package logic

import (
	"encoding/json"
	"os"
	"testing"
)

type goldenCase struct {
	Source string `json:"source"`
	Prog2  string `json:"prog2"`
	Prog1  string `json:"prog1"`
	Want   string `json:"want"`
}

func TestChordProgMultMatchesPython(t *testing.T) {
	data, err := os.ReadFile("testdata/golden.json")
	if err != nil {
		t.Fatal(err)
	}

	var cases []goldenCase
	if err := json.Unmarshal(data, &cases); err != nil {
		t.Fatal(err)
	}
	if len(cases) == 0 {
		t.Fatal("testdata/golden.json has no cases")
	}

	for i, c := range cases {
		if got := ChordProgMult(c.Prog2, c.Prog1); got != c.Want {
			t.Errorf("case %d (%s): ChordProgMult(%q, %q) = %q, want %q", i, c.Source, c.Prog2, c.Prog1, got, c.Want)
		}
	}
}
