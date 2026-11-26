# Meditation Homepage (Testlauf)

Lokale, 100 % offline-fähige Test-Homepage zur Einbindung historischer Vipassana-/Meditationsfotos aus Google Drive.

## Enthaltene Fotos (`assets/photos/`)
- `saya-thetgyi.jpg` – Saya Thetgyi (1873–1945)
- `sayagyi-u-ba-khin.jpg` – Sayagyi U Ba Khin (1899–1971)
- `goenkaji-1924.jpg` – Goenkaji (1924)
- `ladnun-course-1974.jpg` – Kurs in Ladnun (1974)
- `old-dhamma-giri.jpg` – Altes Dhamma Giri
- `course-dhamma-giri.jpg` – Kurs in Dhamma Giri

Quelle: Google Drive (`PADHANA signs / Metta Day Display Boards`).

## Lokal öffnen
- Direkt [index.html](index.html) im Browser öffnen, oder
- per kleinem Webserver:
  ```bash
  python3 -m http.server 8080
  ```

## GitHub Pages (Multi-Branch-Workflow)
Die Seite wird automatisch über `.github/workflows/deploy-pages.yml` auf GitHub Pages veröffentlicht:
- **Live-URL (`main`):** https://stephan1675.github.io/meditation-homepage/
- **`develop`:** https://stephan1675.github.io/meditation-homepage/branches/develop/
- **Claude-Branches (`claude/*`, `*claude*`):** `https://stephan1675.github.io/meditation-homepage/branches/<branch-name>/`

Beim Build (`.github/scripts/build_multibranch.py`) wird automatisch ein zentrierter Branch-Switcher oben auf jeder Seite eingefügt, über den direkt zwischen allen veröffentlichten Branches gewechselt werden kann.

