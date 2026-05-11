# Phase 6 — Skalierung + 3B-Kontrast

**Zeit:** 2 h
**Arbeitsform:** Einzelarbeit — eigener Korpus, eigene Pipeline, eigene Halluzinations-Klassen
**Was am Ende vorliegt:** Predictions auf vollem Korpus (7B + 3B) + drei 3B-Halluzinations-Klassen mit konkreten Beispielen in `notebooks/03_eval.ipynb`

---

## Lernziel

Zwei Dinge auf einmal:

1. **Skalierung** — eure finale Pipeline aus Phase 4 läuft auf eurem vollen Korpus, nicht nur auf den 12 Hand-Gold-Anzeigen
2. **Modellgröße erleben** — 3B-Halluzinationen sind nicht "etwas, was theoretisch passieren kann", sondern etwas, das ihr an eurem eigenen Output seht

Material für die Fachgespräch-Frage zur Modellgrößen-Wahl.

---

## Block 6.1 — Vollständiger 7B-Run (1 h)

Auf gauss, mit eurer finalen Pipeline aus Phase 4 (also nach den Iterationen):

- Datenquelle in der Inferenz-Cell von "12 Hand-Gold-IDs" auf den vollen `daten/eigener_korpus.jsonl` umstellen
- Run starten → `predictions_7b_full.jsonl`

Erwartete Laufzeit: ~3-5 min für 30 Anzeigen, mehr für größere Korpora.

Im Eval-Notebook:

- **Auf den 12 Hand-Gold-Anzeigen** — Per-Field-Accuracy nachrechnen. Bleibt sie stabil zur Phase-4-Baseline? Wenn signifikant abweichend, lohnt sich ein Blick rein.
- **Auf den restlichen Anzeigen ohne Gold** — Schema-Konformität prüfen mit:

  ```bash
  python annotation/validate.py --validate-jsonl predictions_7b_full.jsonl
  ```

  Output ist eine sortierte Liste von Verletzungen pro Feld plus Anzahl JSON-Parse-Fails. Das ist selbst ein Befund über die Pipeline-Stabilität bei größerer Korpus-Vielfalt — notiert die auffälligsten Verletzungstypen im Notebook.

---

## Block 6.2 — 3B als Kontrast (1 h)

**Wechsel auf euler:** neuer Spawn auf euler — Home-Verzeichnis ist NFS-synchronisiert, eure Dateien sind dort auch da.

In `02_extract.ipynb`:
- Modell-Name auf `Qwen/Qwen2.5-3B-Instruct`
- `torch_dtype=torch.float32` zwingend
- Pipeline durchlaufen → `predictions_3b_full.jsonl`

Erwartete Laufzeit: ähnlich wie 7B — die Modell-Größe ändert nicht viel an Inferenz-Zeit, weil die V100 in beiden Fällen nicht der Flaschenhals ist.

**Vergleichs-Mechanik:** drei Quellen per `refnr` joinen — `predictions_7b_full.jsonl`, `predictions_3b_full.jsonl` und euer Hand-Gold. Praktisch: drei DataFrames laden, auf `refnr` mergen, ergibt eine Tabelle mit Spalten wie `homeoffice_3b`, `homeoffice_7b`, `homeoffice_gold`. Wo 3B von 7B abweicht *und* 7B mit Gold übereinstimmt, ist eine wahrscheinliche 3B-Halluzination — solche Fälle sind eure Materialbasis für die drei Klassen. Auf den 60+ Anzeigen ohne Gold könnt ihr nur 3B vs. 7B vergleichen.

**Drei Halluzinations-Klassen** im Notebook — *eigenständig benennen*, nicht generisch:

| Klasse | 3B-Beispiele (Anzeigen-IDs + konkrete Werte) | 7B sagt | Vermutete Ursache |
|---|---|---|---|
| ... | ... | ... | ... |

Eine Klasse ist nicht *"weicht ab"* — sie ist *"weicht **systematisch auf welche Weise** ab"*. Schaut auf Muster über mehrere Anzeigen: was passiert *immer wieder gleich*, wenn 3B vom 7B (oder vom Hand-Gold) abweicht? Findet drei eigene Klassen, jeweils in ein bis zwei Sätzen benannt — abstrakt genug, um auf mehrere Anzeigen zu passen, konkret genug, dass das Muster identifizierbar bleibt.

**Implikation** — würdet ihr das 3B im Produktivszenario einsetzen, und wenn ja, mit welcher Sicherung? (Validator? Stichproben-Review? Eingrenzung auf bestimmte Felder?)
