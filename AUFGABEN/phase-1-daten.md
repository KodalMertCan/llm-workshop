# Phase 1 — Eigenen Korpus aufbauen

**Zeit:** 2 h
**Arbeitsform:** Einzelarbeit — jede:r baut den eigenen Korpus
**Was am Ende vorliegt:** `daten/eigener_korpus.jsonl` mit mindestens 30 Stellenanzeigen + eine kurze Bias-Notiz im Notebook `01_explore.ipynb`

---

## Lernziel

Wo Daten herkommen, ist eine eigene FIDP-Berufsfrage. Bevor wir hier später Pipeline-Aussagen machen, müsst ihr wissen, *welcher Korpus* die Grundlage ist und *welche Eigenschaften* er hat — Quelle, Auswahl, Vollständigkeit, Bias.

---

## Block 1.1 — API-Zugriff bauen (1 h)

Die Bundesagentur für Arbeit betreibt eine offene **Jobbörse-API**. Eure Aufgabe:

1. Findet die API-Dokumentation. Stichwort-Recherche: *"arbeitsagentur jobsuche api"*, *"jobboerse rest api"*. Es gibt offizielle Doku-Seiten und Community-Beispiele.
2. Schreibt ein kleines Python-Skript (oder eine Notebook-Zelle), das:
   - eine Suche ausführt — der Suchbegriff ist eure Wahl. Anregungen: `Fachinformatiker Daten- und Prozessanalyse`, `Data Scientist`, `Datenanalyst`, `Business Intelligence`, `Data Engineer`, … Bleibt im Umfeld datenorientierter IT-Rollen, sonst wird der Korpus zu fachfremd.
   - die Liste der Suchergebnisse durchblättert
   - für jedes Suchergebnis die **Detail-Beschreibung** (den freien Anzeigentext) abruft
   - alles als **JSONL** in `daten/eigener_korpus.jsonl` ablegt (siehe `CHEATSHEETS/jsonl.md`, falls ihr das Format nicht kennt)
3. Sammelt **mindestens 30 Anzeigen**. Nutzt **mehrere Suchanfragen** und variiert dabei (z. B. Ausbildung vs. Festanstellung, verschiedene Berufsbezeichnungen, regional eingeschränkt oder bundesweit), um einen Mix zu kriegen — eine einzige Query reicht nicht.

Hinweise:
- Die API will einen API-Key im Header — den findet ihr in der Doku.
- Baut eine kleine Pause zwischen Requests ein, sonst ratet die API euch raus.
- Speichert pro Anzeige mindestens: `refnr`, `titel`, `firma`, `text` (Beschreibung). Was die API sonst noch liefert (Strukturfelder, Datum, Ort, …), könnt ihr mitschreiben — kann später nützlich werden.


## Block 1.2 — Korpus inspizieren + Bias-Notiz (1 h)

Im Notebook `01_explore.ipynb`:

1. Ladet euren Korpus.
2. Schaut ihn euch an — Verteilungen, was steht typisch drin, was variiert stark? Beispiele:
   - Längen-Verteilung der Beschreibungstexte
   - Welche Firmen tauchen mehrfach auf?
   - Welche Berufsbezeichnungen / Senioritätsstufen sind drin?
   - Welche Strukturfelder hat die API überhaupt mitgeliefert, und wie oft sind die wirklich befüllt?
3. Schreibt eine **Bias-Notiz** in einer Markdown-Zelle. **5-7 Sätze, frei formuliert.** Was ist an eurem Korpus systematisch schief — und was bedeutet das für jede Aussage, die ihr später macht? Konkret werden, mit Zahlen oder Anzeigen-IDs, nicht generisch.

Was ist hier mit "Bias" gemeint? Alles, was bewirkt, dass euer Korpus **nicht repräsentativ** für "Stellenanzeigen in Deutschland" ist: eure Suchanfragen-Auswahl, Plattform-Effekte (was Firmen *bei dieser API* einstellen), Sprache, Region, Berufsfeld, Vertragsart, … Findet eure eigenen Punkte am eigenen Material.

