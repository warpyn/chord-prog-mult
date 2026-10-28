document.addEventListener("alpine:init", () => {
  const fields = [
    { key: "Song", label: "Song" },
    { key: "Artist", label: "Artist" },
    { key: "Section", label: "Section" },
    { key: "Progression", label: "Progression" },
    { key: "RomanNumerals", label: "Roman Numerals" },
  ];

  Alpine.data("catalog", () => ({
    songs: JSON.parse(document.getElementById("catalog-data").textContent),
    fields,
    column: "symbols",
    selected: [],
    query: "",
    sortKey: "",
    sortDescending: false,

    get visibleIndices() {
      const query = this.query.trim().toLowerCase();
      const indices = this.songs
        .map((_, index) => index)
        .filter((index) => fields.some((field) => this.songs[index][field.key].toLowerCase().includes(query)));

      if (this.sortKey) {
        const direction = this.sortDescending ? -1 : 1;
        indices.sort((a, b) => direction * this.songs[a][this.sortKey].localeCompare(this.songs[b][this.sortKey]));
      }
      return indices;
    },

    get chordsLabel() {
      return this.column === "roman" ? "Roman Numerals" : "Progression";
    },

    chords(index) {
      return this.column === "roman" ? this.songs[index].RomanNumerals : this.songs[index].Progression;
    },

    toggle(index) {
      if (this.selected.includes(index)) {
        this.selected = this.selected.filter((selectedIndex) => selectedIndex !== index);
      } else {
        this.selected.push(index);
      }
    },

    sortBy(key) {
      if (this.sortKey === key) {
        this.sortDescending = !this.sortDescending;
      } else {
        this.sortKey = key;
        this.sortDescending = false;
      }
    },

    sortIndicator(key) {
      if (this.sortKey !== key) {
        return "↕";
      }
      return this.sortDescending ? "▼" : "▲";
    },
  }));
});
