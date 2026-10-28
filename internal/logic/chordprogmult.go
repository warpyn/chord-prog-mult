package logic

import "strings"

const (
	duplicateChords = "Invalid Input: Duplicate Chords Found"
	noProgression   = "Invalid Input: No Progression Detected"
)

func ChordProgMult(prog2, prog1 string) string {
	chords1 := strings.Split(prog1, " ")
	chords2 := strings.Split(prog2, " ")

	if hasDuplicates(chords1) || hasDuplicates(chords2) {
		return duplicateChords
	}
	if len(chords1) == 0 || len(chords2) == 0 {
		return noProgression
	}

	symbols, numbered := numberChords(chords1, chords2)
	next1 := successors(numbered[0], len(symbols))
	next2 := successors(numbered[1], len(symbols))

	product := make([]int, len(symbols))
	for n := range product {
		product[n] = next2[next1[n]]
	}

	return formatCycles(cycles(product), symbols)
}

func hasDuplicates(chords []string) bool {
	seen := make(map[string]bool, len(chords))
	for _, chord := range chords {
		if seen[chord] {
			return true
		}
		seen[chord] = true
	}
	return false
}

func numberChords(progressions ...[]string) (symbols []string, numbered [][]int) {
	numberOf := make(map[string]int)
	for _, chords := range progressions {
		numbers := make([]int, len(chords))
		for i, chord := range chords {
			n, seen := numberOf[chord]
			if !seen {
				n = len(symbols)
				numberOf[chord] = n
				symbols = append(symbols, chord)
			}
			numbers[i] = n
		}
		numbered = append(numbered, numbers)
	}
	return symbols, numbered
}

func successors(progression []int, size int) []int {
	next := make([]int, size)
	for n := range next {
		next[n] = n
	}
	for i, n := range progression {
		next[n] = progression[(i+1)%len(progression)]
	}
	return next
}

func cycles(permutation []int) [][]int {
	visited := make([]bool, len(permutation))
	var result [][]int
	for start := range permutation {
		if visited[start] {
			continue
		}

		var cycle []int
		for n := start; !visited[n]; n = permutation[n] {
			visited[n] = true
			cycle = append(cycle, n)
		}
		result = append(result, cycle)
	}
	return result
}

func formatCycles(cycles [][]int, symbols []string) string {
	var b strings.Builder
	for _, cycle := range cycles {
		chords := make([]string, len(cycle))
		for i, n := range cycle {
			chords[i] = symbols[n]
		}
		b.WriteString("(" + strings.Join(chords, " ") + ")")
	}
	return b.String()
}
