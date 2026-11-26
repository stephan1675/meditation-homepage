# Projekt-Gedächtnis: Meditation Homepage

## 1. Projekt-Übersicht
- **Zweck:** Erster End-to-End-Testlauf der KI-Zentrale: Suche in Google Drive, Download in lokalen Asset-Ordner und Aufbau einer statischen Galerie-Homepage.
- **Stack:** Reines HTML5 / CSS3 / Vanilla JS (keine Build-Tools, keine externen CDNs).
- **Quelle der Bilder:** Google Drive (`PADHANA signs / Metta Day Display Boards / Chain of teachers` & `History long courses`).
- **Live-URL:** `https://stephan1675.github.io/meditation-homepage/` (Multi-Branch GitHub Pages).

## 2. Dateien & Features
- `index.html` & `styles.css`: Responsive Fotogalerie mit Kategorie-Filter (*Lehrer-Linie*, *Historische Kurse*) und Lightbox.
- `assets/photos/*.jpg`: 6 heruntergeladene Archivaufnahmen.
- **Theme (Claude):** Hell/Dunkel-Umschalter im Hero (`#theme-toggle`), `data-theme` auf `<html>`, `localStorage["theme"]` + `prefers-color-scheme`-Fallback, Anti-Flash-Inline-Script im `<head>`, CSS-Variablen unter `:root[data-theme="dark"]`; Lightbox bleibt dunkel.
- **Infosektion „Über dieses Archiv“** (`#about`): Kurztext zur Linie & frühen Kursen (Ladnun 1974, Dhamma Giri 1976) + vertikale Lehrer-Timeline (`.lineage`).
- `.github/workflows/deploy-pages.yml` & `.github/scripts/build_multibranch.py`: Multi-Branch-GitHub-Pages-Workflow für `main`, `develop` und `*claude*`-Branches inkl. zentriertem Branch-Switcher.
- `AGENTS.md`, `CLAUDE.md` (`@AGENTS.md`-Pointer) & `.agents/skills/checkpoint/SKILL.md` / `.claude/skills/checkpoint/SKILL.md`: Portable Regeln und `/checkpoint`-Skill aus `stephan1675/project-template`.

## 3. Aktueller Stand & Nächste Schritte
- **Stand (2026-11-26):** `feature/claude-info-section` (Theme-Toggle + Infosektion) sowie `/checkpoint`-Skill & portable Agent-Regeln sind in `develop` und `main` integriert und live auf GitHub Pages.
- **Offen:** Bei Bedarf weitere Fotos (z. B. Motorrad-Bilder aus bestimmtem Drive-Ordner) oder Feinschliff auf einem neuen `feature/*`-Branch ergänzen.
