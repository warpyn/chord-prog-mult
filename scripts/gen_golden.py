import csv
import json
import sys
from pathlib import Path

EDGE_INPUTS = [
    "C G",
    "F Bb C",
    "G C",
    "C G Am F",
    "Am F C G",
    "Dm G",
    "E A",
    "C",
    "C C",
    "C G C",
    "C  G",
    "C G ",
    " C G",
    "C  G  ",
    " ",
    "",
]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: gen_golden.py <path to python-final checkout>")

    checkout = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(checkout))
    from algorithms.alg_chordprogmult import chordProgMult

    with open(checkout / "datasets" / "prog_catalog.csv", encoding="utf-8-sig", newline="") as f:
        songs = list(csv.DictReader(f))

    input_sets = [
        ("catalog symbols", [song["Progression"] for song in songs]),
        ("catalog roman", [song["Roman Numerals"] for song in songs]),
        ("edge", EDGE_INPUTS),
    ]

    cases = []
    for source, progressions in input_sets:
        for prog2 in progressions:
            for prog1 in progressions:
                cases.append({
                    "source": source,
                    "prog2": prog2,
                    "prog1": prog1,
                    "want": chordProgMult(prog2, prog1),
                })

    lines = ",\n".join(json.dumps(case, ensure_ascii=False) for case in cases)
    sys.stdout.write("[\n" + lines + "\n]\n")


if __name__ == "__main__":
    main()
