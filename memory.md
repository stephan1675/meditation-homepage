# Projekt-Gedächtnis: Meditation Homepage

## 1. Projekt-Übersicht
- **Zweck:** Erster End-to-End-Testlauf der KI-Zentrale: Suche in Google Drive, Download in lokalen Asset-Ordner und Aufbau einer statischen Galerie-Homepage.
- **Stack:** Reines HTML5 / CSS3 / Vanilla JS (keine Build-Tools, keine externen CDNs).
- **Quelle der Bilder:** Google Drive (`PADHANA signs / Metta Day Display Boards / Chain of teachers` & `History long courses`).

## 2. Dateien
- `index.html` & `styles.css`: Responsive Fotogalerie mit Kategorie-Filter (*Lehrer-Linie*, *Historische Kurse*) und Lightbox.
- `assets/photos/*.jpg`: 6 heruntergeladene Archivaufnahmen.
- **Theme (Claude, `feature/claude-info-section`):** Hell/Dunkel-Umschalter im Hero (`#theme-toggle`). Theme als `data-theme` auf `<html>`, gespeichert in `localStorage["theme"]`; ohne Eintrag gilt `prefers-color-scheme`. Inline-Script im `<head>` verhindert Aufblitzen. Dark-Werte in `:root[data-theme="dark"]` (`styles.css`); hartkodierte Farben (Hero-Gradient, Badge, aktiver Filter, Hover-Schatten) auf Variablen umgestellt. Lightbox bleibt bewusst immer dunkel.
- **Infosektion „Über dieses Archiv“** (`#about`, zwischen `<main>` und Footer): Kurztext zur Linie & frühen Kursen (Ladnun 1974, Dhamma Giri 1976) + vertikale Lehrer-Timeline (`.lineage`), mobil einspaltig.

## 3. Aktueller Stand & Nächste Schritte
- **Stand (2026-11-26):** Lokal angelegt und als privates GitHub-Repo [stephan1675/meditation-homepage](https://github.com/stephan1675/meditation-homepage) (`main`) gepusht.
- **Offen:** Claude-Feature (Theme-Toggle + Infosektion) auf `feature/claude-info-section` prüfen und freigeben (kein Merge ohne Freigabe).
