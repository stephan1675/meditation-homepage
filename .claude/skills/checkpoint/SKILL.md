---
name: checkpoint
description: Verdichtet den aktuellen Projekt- und Session-Stand kompakt in memory.md (<150 Zeilen) und erstellt einen kurzen Resume-Prompt für eine frische Session oder den Agent-Wechsel (Antigravity <-> Claude). Nutzen bei langen Sessions, auf Mobile/Cloud ohne /compact oder vor einem Handoff.
---

# Checkpoint & Cross-Agent Handoff

Führe diesen Ablauf aus, wenn der Nutzer `/checkpoint`, „mach einen Checkpoint“, „Handoff vorbereiten“ oder „Stand für neue Session sichern“ anfordert:

## Schritte
1. **Status prüfen (kurz):** `git status -sb` und ggf. `git diff --stat` (keine großen Diffs dumpen).
2. **`memory.md` in-place aktualisieren (Deutsch, strikt < 150 Zeilen):**
   - Veraltete Angaben ersetzen (kein chronologisches Log anhängen).
   - Festhalten: aktiver Branch & uncommitted Status, erreichte Meilensteine, verifizierte Ergebnisse/Tests, offene Bugs/Blocker, getroffene Architekturentscheidungen und die konkreten nächsten 1–3 Schritte.
   - Keine Secrets, Tokens oder persönlichen lokalen Pfade eintragen.
3. **Kompakten Resume-Prompt ausgeben (Deutsch, max. 10 Zeilen als Codeblock):**
   - Enthält: Repo/Branch, Verweis auf `AGENTS.md` + `memory.md`, exakter aktueller Fokus und den unmittelbaren nächsten Schritt.
   - Damit kann der Nutzer sofort eine neue, ballastsfreie Session in **Antigravity** oder **Claude** (Desktop, Web oder Handy) starten.
4. **Nicht automatisch committen oder mergen**, außer der Nutzer hat explizit darum gebeten.
