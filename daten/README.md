# daten/

Hier landet euer **eigener Korpus** aus Phase 1.

- `eigener_korpus.jsonl` — mindestens 30 Stellenanzeigen aus der Bundesagentur-Jobbörse-API. Eine Anzeige pro JSONL-Zeile mit Mindestfeldern `refnr`, `titel`, `firma`, `text`. Format-Hinweise im [`CHEATSHEETS/jsonl.md`](../CHEATSHEETS/jsonl.md).

Sonst nichts. Pipeline-Outputs (`predictions*.jsonl`) bleiben über `.gitignore` aus dem Verzeichnis raus, weil sie zu groß werden — die liegen während der Arbeit auf dem Jupyterhub-Server, nicht im Repo.
