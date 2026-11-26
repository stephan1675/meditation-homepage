# Projekt-Gedächtnis: Meditation Homepage

## 1. Projekt-Übersicht
- **Zweck:** Erster End-to-End-Testlauf der KI-Zentrale: Suche in Google Drive, Download in lokalen Asset-Ordner und Aufbau einer statischen Galerie-Homepage.
- **Stack:** Reines HTML5 / CSS3 / Vanilla JS (keine Build-Tools, keine externen CDNs).
- **Quelle der Bilder:** Google Drive (`PADHANA signs / Metta Day Display Boards / Chain of teachers` & `History long courses`).

## 2. Dateien
- `index.html` & `styles.css`: Responsive Fotogalerie mit Kategorie-Filter (*Lehrer-Linie*, *Historische Kurse*) und Lightbox.
- `assets/photos/*.jpg`: 6 heruntergeladene Archivaufnahmen.
- `.github/workflows/deploy-pages.yml` & `.github/scripts/build_multibranch.py`: Multi-Branch-GitHub-Pages-Workflow für `main`, `develop` und Claude-Branches (`claude/*`, `*claude*`) inkl. zentriertem Branch-Switcher oben.

## 3. Aktueller Stand & Nächste Schritte
- **Stand (2026-11-26):** Repository [stephan1675/meditation-homepage](https://github.com/stephan1675/meditation-homepage) auf `public` gestellt, `develop`-Branch angelegt und Multi-Branch-Deployment auf GitHub Pages (`https://stephan1675.github.io/meditation-homepage/`) aktiviert.
- **Offen:** Claude-CLI-Feature auf `feature/claude-info-section` prüfen und freigeben (live unter `branches/feature/claude-info-section/` über den Branch-Switcher erreichbar).

