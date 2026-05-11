# Frontier-LLM-Workflow — Cheatsheet

**Wann ihr das braucht:** Phase 5 — Mensch ↔ Frontier-LLM-Vergleich.

## Welcher Chat?

Empfehlung: **Claude (claude.ai) mit Opus 4.6 oder höher**, alternativ **ChatGPT mit GPT-5 oder höher**.

Begründung: beide produzieren JSON-Output mit Schema-Adherence > 95 %. Andere Modelle (kleinere offene Modelle, Web-Mistral o. ä.) sind verlässlich nur unter API-Steuerung — im Web-Chat oft nicht zuverlässig genug.

Notiert die genaue Modell-Version im Run-Header von `04_frontier_compare.ipynb` (z. B. `claude-opus-4-7`).

## Eingabe-Block-Aufbau

Der Chat bekommt **einen Turn** — Copy-Paste in das erste Eingabefeld. Welche Blöcke der Prompt enthalten muss, steht hier; den genauen Wortlaut formuliert ihr selbst. Prompt-Engineering ist Lerngegenstand dieser Phase — ein wackeliger Prompt produziert ein wackeliges κ und färbt eure Make-or-Buy-Aussage.

Struktur-Skelett:

```
[Rolle + Anweisung — präzise, kein Spielraum für Begleittext im Output]

SCHEMA:
[6 Felder mit erlaubten Werten — kompakte Form aus SCHEMA.md]

DEFINITIONEN:
[die nicht-trivialen Negativ-Definitionen aus SCHEMA.md, die für die Annotation entscheidend sind]

BEISPIELE:
[3 Few-Shot-Paare aus eurem Hand-Gold: Anzeigentext + erwartetes JSON]

AUFGABE:
[Annotations-Anweisung, Output-Format-Spec, id-Feld-Vorgabe]

ANZEIGEN:
=== id: <refnr_1> ===
[Volltext Anzeige 1]

=== id: <refnr_2> ===
[Volltext Anzeige 2]

... (insgesamt 12 Anzeigen)
```

**Drei Anker, die das Output-Format stabil halten** — diese Punkte gehören in eurer Formulierung in den Prompt:

1. **Explizite Anweisung "JSON-Array, kein Text davor oder danach"** — sonst schreibt Claude *"Hier sind die annotierten Anzeigen:"* und das Parsing wird mühsam.
2. **3 Few-Shot-Beispiele** aus eurem Hand-Gold — in derselben Form, in der ihr selbst annotiert habt. Zwingt das Modell auf eure Schema-Interpretation, nicht auf eine "naheliegende".
3. **`id`-Feld in jedem Output-Objekt** — sonst wird die Zuordnung beim κ-Compute mühsam (Reihenfolge alleine ist fragil bei 12 Records).

Wenn euer Prompt schwächer wirkt als der eines Mitschülers (niedrigeres κ trotz vergleichbarer Anzeigen): *das* ist selbst ein Befund — geht in die Make-or-Buy-Reflexion ein als Frage *"war das Frontier wirklich schlechter, oder war mein Prompt nicht stabil genug?"*.

## Workflow Schritt für Schritt

1. Eure 12 Hand-Gold-Anzeigen aus Phase 2 — Volltexte aus eurem Korpus ziehen
2. 3 davon als Few-Shot-Beispiele wählen (Mix aus Ausbildung + Festanstellung empfohlen)
3. Eingabe-Block bauen — Schema, 3 Beispiele, 12 Anzeigen
4. In claude.ai oder ChatGPT eingeben, Antwort abwarten
5. JSON-Array kopieren, in `frontier_predictions.json` speichern
6. In `04_frontier_compare.ipynb` laden, in CSV umwandeln → `annotation/frontier_gold.csv` (manuell oder per Mini-Script)
7. `python annotation/validate.py annotation/frontier_gold.csv` — Schema-Konformität prüfen
8. κ rechnen: `python annotation/validate.py annotation/meine_gold.csv --kappa-against annotation/frontier_gold.csv`

## Schema-Verletzungen sind Standard, nicht Ausnahme

Häufig:
- Wert außerhalb der Liste (z. B. `"homeoffice": "möglich"`)
- skills_top3 hat 4 oder 5 Einträge
- gehalt_min_eur als String statt int

Eskalations-Strategie im selben Chat:

> *"Anzeige X hat homeoffice=möglich. Das ist nicht im Schema. Der Wert muss aus
> [ja, teilweise, nein, remote, nicht_genannt] kommen. Korrigiere bitte und
> gib die korrigierten Anzeigen erneut als JSON-Array."*

In der Regel reicht ein Korrektur-Turn. Wenn nach zwei Korrekturen immer noch Verletzungen kommen: **Schema-Schwäche in eurer Definition** — das ist ein Befund, kein Bug. Notiert im Memo.

Alternativ: in der CSV manuell mappen (`"möglich"` → `"teilweise"`, `"freelance"` → `"selbstaendig"`) und die Mapping-Tabelle dokumentieren — dokumentations-aufwändiger, vermeidet aber Korrektur-Turns.

## Datenschutz / DSGVO

Der Bundesagentur-Korpus ist **öffentlich** — Anzeigen sind ohnehin im Web abrufbar.

Trotzdem zwei Regeln:

1. **Keine Anzeigen aus eurem Ausbildungsbetrieb** in den Web-Chat geben — die sind nicht öffentlich.
2. **Kein Login-Account auf den Schul-Computern speichern.** Logout nach Sitzung.

## Reproduzierbarkeit

Im Run-Header von `04_frontier_compare.ipynb`:

| | |
|---|---|
| Modell-Version | z. B. `claude-opus-4-7` |
| Datum | YYYY-MM-DD |
| Prompt-Variante | "v1 mit 3 Few-Shots aus IDs <a, b, c>" |
| Anzahl Korrektur-Turns | 0 / 1 / 2 |
| Auffälligkeiten | z. B. "skills_top3 oft 4 Einträge — Korrektur nötig" |

Damit ist euer Frontier-Run reproduzierbar — und ein Wiederholen mit anderem Modell (Opus vs. ChatGPT) wird leichter vergleichbar.

## Number-Receipt-Form fürs Memo + Fachgespräch

> *"Mein Mensch-↔-Frontier-κ auf `erfahrungslevel` (n=12) ist 0,55 — moderat. Die zwei Disagreement-Fälle waren beide *Werkstudent → mid* (LLM) vs. *Werkstudent → junior* (ich). Das ist kein Modellfehler, sondern Schema-Lücke: 'Werkstudent' ist im Schema unter `vertragsart`, aber das `erfahrungslevel`-Mapping ist nicht definiert."*

Wert + Stichprobe + Disagreement-Mechanismus + Implikation. So wird die Make-or-Buy-Argumentation im Memo tragfähig.
