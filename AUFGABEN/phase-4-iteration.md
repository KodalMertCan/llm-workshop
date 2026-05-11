# Phase 4 — Iteration: Pipeline verbessern (KERNSTÜCK)

**Zeit:** 4 h
**Arbeitsform:** Einzelarbeit — eigene Pipeline, eigene Hypothese, eigene Iterationen
**Was am Ende vorliegt:** Iterations-Tabelle (mind. 2 Zeilen — Hypothese / Aktion / Δ / Diagnose) in `notebooks/03_eval.ipynb` + Synthese in eigenen Worten

---

## Lernziel

Ihr lernt, **Schema-Fehler von Modell-Fehlern von Pipeline-Fehlern zu trennen**. Wenn ihr das könnt, könnt ihr den Workflow auf jede strukturelle Extraktion übertragen — das ist der berufstragende Teil der LS.

---

## Block 4.1 — Hebel wählen (0,5 h)

Aus Phase 3 habt ihr zwei schwache Felder + eine Vermutung pro Feld (Schema/Modell/Pipeline). Das ist eure Hypothese.

Wählt **mindestens zwei Iterationen** aus dieser Liste:

- **Prompt-Klarstellung** — Schema-Beschreibung im Prompt schärfen, ambivalente Werte explizit abgrenzen (z. B. *"`teilweise` nur bei expliziter Hybrid-Erwähnung, sonst `nicht_genannt`"*). Sinnvoll, wenn euer schwaches Feld eine kategorische Klassifikation ist und das Modell oft *fast richtig* falsch liegt.
- **Few-Shot-Beispiele** — 2-3 typische Anzeigen aus eurem Hand-Gold als `user`/`assistant`-Paare *vor* dem aktuellen Anzeigen-Turn in die `messages`-Liste einbauen. Sinnvoll, wenn das Modell das *Format* der Antwort verfehlt (zu lange Listen, halluzinierte Werte). Achtung: Few-Shots verlängern den Prompt — Truncation muss enger werden.
- **Pre-Processing / smartere Truncation** — statt Head-Truncation gezielt Textfenster um Schlüsselwörter ausschneiden (z. B. ±200 Zeichen um `Gehalt`, `€`, `Homeoffice`, `remote`). Sinnvoll, wenn der relevante Wert systematisch *nach* den ersten 2000 Zeichen steht (lange Anzeigen mit "Wir suchen…"-Boilerplate vorne).
- **Modellgröße** — 3B als Negativ-Kontrast auf euler (oder 14B falls verfügbar). Sinnvoll als Sanity-Check: wenn das größere Modell die Schwäche behebt, ist's Modell-Limit; wenn auch das größere scheitert, ist's vermutlich Schema- oder Pipeline-Lücke. *Hinweis: 3B kommt sowieso in Phase 6 — wer hier den 3B-Hebel zieht, kann Phase 6.2 entsprechend verkürzen.*

Welche zwei (oder mehr) ihr wählt, ist eure Entscheidung — abhängig von eurer Hypothese aus Phase 3. Diese Wahl gehört in eure Iterations-Tabelle (siehe 4.4).

---

## Block 4.2 — Iteration A (1,5 h)

In `notebooks/03_eval.ipynb`:

1. **Hypothese-Cell vor der Iteration** — schreibt auf, *was ihr erwartet*: welches Feld, welche Δ-Größe, warum
2. **Implementieren** — Prompt anpassen, Few-Shots einbauen, Truncation umbauen, etc.
3. **Pipeline neu laufen lassen** → speichern unter eigenem Namen (`predictions_iterA.jsonl` für A, `predictions_iterB.jsonl` für B). Nicht die Baseline `predictions.jsonl` aus Phase 3 überschreiben — das Eval-Notebook braucht alle Stände nebeneinander, um Δ zu rechnen. Run-Header-Cell jeweils mit neuem Datum + Iteration-Tag.
4. **Per-Field-Accuracy neu rechnen**
5. **Auswertung-Cell** — Δ pro Feld eintragen, Befund in eigenen Worten

> Auch Δ = 0 oder negative Δ sind valide Befunde — *was sagt das* über eure Hypothese? Eine ehrliche "Iteration brachte nichts"-Auswertung ist mehr wert als ein zurechtgebogenes "irgendwas hat sich verbessert".

---

## Block 4.3 — Iteration B (1,5 h)

Gleicher Ablauf wie 4.2 — neue Hypothese-Cell, Implementierung, Run, Auswertung.

Wenn ihr nach Iteration A unsicher seid, ob eure Diagnose stimmt: kurz mit dem Lehrer drüber reden, bevor ihr Iteration B startet. 1,5 h Iteration mit falsch zugeordneter Diagnose ist verschwendete Zeit.

---

## Block 4.4 — Synthese (0,5 h)

**Iterations-Tabelle** in `03_eval.ipynb`:

| Iteration | Hypothese | Aktion | Δ Gesamt | Δ schwächstes Feld | Diagnose (Schema/Modell/Pipeline) |
|---|---|---|---|---|---|
| Baseline | — | — | — | — | — |
| A | ... | ... | ... | ... | ... |
| B | ... | ... | ... | ... | ... |

**Synthese** in eigenen Worten (kein Schablonentext):

- Welcher der drei Fehler-Typen war in *eurem* Setup die häufigste Ursache?
- Was wäre **nicht** durch Iteration lösbar — wo ist Modell oder Schema die harte Grenze?
- Würdet ihr im Berufsalltag *alle* Probleme fixen, oder gibt es Fehler, die "gut genug" sind? Wo liegt eure Schwelle?

> **Statistische Selbstkritik (optional, aber wertvoll fürs Fachgespräch):** Bei n=12 entspricht eine einzelne falsch klassifizierte Anzeige ≈ 8,3 Pt. Rechnet eure Δ in absolute Anzahlen zurück — ab welcher absoluten Differenz nehmt ihr einen Befund ernst, ab welcher ist es Rauschen? Wer das durchdenkt, hat eine Schwellwert-Logik, die im Fachgespräch trägt.
