# Phase 5 — Frontier-LLM als Annotator + Make-or-Buy

**Zeit:** 3 h
**Arbeitsform:** Einzelarbeit — eigene 12 Anzeigen aus Phase 2, eigenes κ, eigenes Memo
**Was am Ende vorliegt:** `annotation/frontier_gold.csv` (12 Anzeigen, von Claude/ChatGPT annotiert) + κ Mensch ↔ Frontier in `notebooks/04_frontier_compare.ipynb` + 1-Seiter Make-or-Buy-Memo (`memo_make_or_buy.md`)

---

## Lernziel

"94 % Accuracy" — wann ist ein Frontier-LLM (Claude Opus, ChatGPT) ein vertrauenswürdiger Annotator? Ihr trefft am Ende eine **Methoden-Entscheidung**: würdet ihr im echten Projekt die restlichen Anzeigen vom Frontier-LLM annotieren lassen oder selbst — und *warum* (mit eigenem κ als Beleg)?

Make-or-Buy ist ein berufsechter Anker.

---

## Block 5.1 — Frontier annotiert dieselben 12 Anzeigen (1,5 h)

Cheatsheet vorab lesen: `CHEATSHEETS/frontier-llm-workflow.md` (Eingabe-Block-Format, DSGVO-Hinweise).

**Setup:**

1. Dieselben 12 Anzeigen wie in Phase 2
2. Eingabe-Block bauen: Schema + 2-3 Few-Shot-Beispiele + 12 Anzeigen
3. In Claude (claude.ai, Opus 4.6+) **oder** ChatGPT (GPT-4o+) eingeben
4. Output-JSON → `annotation/frontier_gold.csv` — entweder **manuell** in Excel/LibreOffice (12 Zeilen, geht in 5 min, gut für direkten Sichtcheck der Werte) oder **per Mini-Script** in einer Notebook-Zelle (`json.loads(...)` → DataFrame → `to_csv()`). Beides legitim, dokumentiert die Wahl im Notebook.

In der Run-Header-Cell von `04_frontier_compare.ipynb` festhalten: Modell-Version, Prompt-Variante, Anzahl Korrektur-Turns (falls Schema-Verletzungen nachgefragt werden mussten).

**DSGVO:** nur die Bundesagentur-Anzeigen ans Frontier geben — keine Anzeigen aus eurem Ausbildungsbetrieb, falls da welche im Korpus gelandet wären.

---

## Block 5.2 — κ Mensch ↔ Frontier (0,5 h)

**Hypothese-Cell vor κ-Compute:**
- Was schätzt ihr ist das Gesamt-κ?
- Bei welchem Feld erwartet ihr das niedrigste κ — warum?

```bash
python annotation/validate.py annotation/meine_gold.csv --kappa-against annotation/frontier_gold.csv
```

**Schema-Verletzungen sind Standard, nicht Ausnahme** — das Frontier-LLM erfindet gerne Werte wie `homeoffice="möglich"`, `vertragsart="freelance"`, `gehalt_zeitraum="auf Anfrage"`. Pro Verletzung trefft ihr eine Entscheidung:

- **Mappen**, wenn die Bedeutung eindeutig ist (`"möglich"` → `"teilweise"`, `"freelance"` → `"selbstaendig"`) — Mapping-Tabelle ins Notebook.
- **Nachfragen** im selben Web-Chat, wenn unklar — Korrektur-Turns zählt ihr im Run-Header mit.
- **Nicht selbst raten** (z. B. pauschal `"nicht_genannt"` einsetzen) — das verfälscht das κ.

Zwei bis fünf Verletzungen bei 12 Anzeigen sind normal. Deutlich mehr → Prompt für Block 5.1 nachschärfen und neu laufen.

**κ-Tabelle** im Notebook: pro Feld κ-Wert + bei welchen Anzeigen-IDs ihr und das Frontier auseinanderlagen.

Drei **konkrete Disagreements** durchsprechen:

- An welcher Anzeige?
- Welcher Wert habt ihr, welcher das Frontier?
- **Wer hatte recht?** Begründung — das ist die Stelle, an der ihr euer eigenes Schema reflektiert. "Frontier sah etwas, das mein Schema nicht abbildet" ist ein anderer Befund als "Frontier hat halluziniert".

---

## Block 5.3 — Make-or-Buy-Memo (1 h)

Anlegen als `memo_make_or_buy.md` im Repo-Root (eine Seite, frei formuliert).

Adressat ist eure Projektleitung im (fiktiven) FIDP-Projekt — ihr empfehlt, wie die restlichen 60+ Anzeigen annotiert werden sollen.

Inhalt mindestens:

1. **Eure Empfehlung** — Frontier macht alle, Mensch macht alle, oder Hybrid mit konkreter Aufteilung
2. **Begründung an eurem κ** — auf welchen Feldern vertraut ihr dem Frontier, auf welchen nicht?
3. **Schwellwert-Logik** — wo wäre eure Grenze? Was müsste anders sein, damit ihr anders entscheidet?
4. **Risiko-Sicherung** — wenn ihr falsch liegt, was geht schief? Welche Stichproben-Kontrolle baut ihr ein?

Eine Seite reicht — substantielle Sätze sind besser als Aufzählungen.

> Diese Memo ist die Grundlage für die Fachgespräch-Frage zur Make-or-Buy-Entscheidung. Wer hier konkret wird (eigene κ-Werte als Beleg, eigene Schwelle), hat das Fachgespräch in dieser Kategorie schon halb gewonnen.
