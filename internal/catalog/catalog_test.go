package catalog

import "testing"

func TestLoad(t *testing.T) {
	songs, err := Load()
	if err != nil {
		t.Fatal(err)
	}

	if len(songs) != 34 {
		t.Errorf("len(songs) = %d, want 34", len(songs))
	}

	first := Song{Song: "We Never Change", Artist: "Coldplay", Section: "Verse Part 1", Progression: "F#m E", RomanNumerals: "vi V"}
	if songs[0] != first {
		t.Errorf("songs[0] = %+v, want %+v", songs[0], first)
	}

	last := Song{Song: "Imagine", Artist: "John Lennon", Section: "Bridge Alt", Progression: "F G C E7", RomanNumerals: "IV V I III7"}
	if songs[len(songs)-1] != last {
		t.Errorf("last song = %+v, want %+v", songs[len(songs)-1], last)
	}
}

func TestLoadKeepsTrailingSpace(t *testing.T) {
	songs, err := Load()
	if err != nil {
		t.Fatal(err)
	}

	chorus := songs[2]
	if chorus.Section != "Chorus" || chorus.Progression != "Aadd9 C#m7 " {
		t.Errorf("songs[2] = %+v, want Chorus with progression %q", chorus, "Aadd9 C#m7 ")
	}
}

func TestChords(t *testing.T) {
	song := Song{Progression: "Dm G C", RomanNumerals: "ii V I"}

	tests := []struct {
		column Column
		want   string
	}{
		{Symbols, "Dm G C"},
		{Roman, "ii V I"},
	}
	for _, tt := range tests {
		if got := song.Chords(tt.column); got != tt.want {
			t.Errorf("Chords(%q) = %q, want %q", tt.column, got, tt.want)
		}
	}
}
