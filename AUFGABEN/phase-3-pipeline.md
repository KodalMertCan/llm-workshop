# Phase 3 — Pipeline selbst bauen

**Zeit:** 3 h (gauss, 7B-Modell)
**Arbeitsform:** Einzelarbeit — jede:r baut eine eigene Pipeline auf eigenem Korpus
**Was am Ende vorliegt:** lauffähige Pipeline in `notebooks/02_extract.ipynb` + Per-Field-Accuracy-Tabelle in `notebooks/03_eval.ipynb` gegen euer Hand-Gold

---

## Lernziel

Ihr bringt das lokale 7B-Modell zum Laufen und messt seine erste Extraktion gegen euer eigenes Hand-Gold aus Phase 2. Ergebnis: konkrete Zahlen-Belege, gegen die ihr ab Phase 4 iteriert.

---

## Block 3.1 — Pipeline bauen (2 h)

**Setup:** Jupyterhub-Spawn auf gauss, VPN aktiv falls nötig (siehe `CHEATSHEETS/gpu-zugang.md`).

In `notebooks/02_extract.ipynb` baut ihr die Pipeline selbst — kein Skelett zum Ausfüllen. Bausteine, die sie braucht:

1. **Modell-Load** — `Qwen/Qwen2.5-7B-Instruct`, mit `torch_dtype=torch.float32` (V100-Hardware-Constraint, siehe Cheatsheet)
2. **Prompt** — euer Schema in den System-Prompt einbauen. Tipp: ein **konkretes Beispiel-JSON** im Prompt (Few-Shot oder im System-Block) stabilisiert das Modell deutlich besser als nur eine Schema-Beschreibung in Worten.
3. **Chat-Template** — der Tokenizer kennt das richtige Format, Mini-Snippet im Cheatsheet
4. **Truncation** — initial reicht einfache Head-Truncation auf das Kontextfenster (~2000 Zeichen). Smartere Strategien sind Material für Phase 4.
5. **Inferenz-Schleife** — pro Anzeige Prompt → generate → JSON aus der Antwort **robust extrahieren** → in `predictions.jsonl` speichern. Achtung: das Modell umrahmt das JSON gerne mit Prosa (*"Hier ist das Ergebnis: {...} Hoffe das hilft!"*) — direktes `json.loads(response)` knallt dann. Mit Regex (`re.search(r"\{.*\}", output, re.DOTALL)`) das JSON-Objekt herauspulen, sonst habt ihr 30 % Parse-Fails ohne ersichtlichen Grund.

Cheatsheet: `CHEATSHEETS/transformers-konzepte.md` — Modell-Namen, Chat-Template, "device_map nicht"-Hinweis.

**Run-Header-Cell** am Notebook-Anfang: Modell, Server, GPU-Index, Datum. Damit der Run nachvollziehbar ist.

Wenn ihr nach 90 min stuck seid: Lehrer ansprechen.

---

## Block 3.2 — Erste Extraktion + Eval (1 h)

Pipeline auf eure **12 Hand-Gold-Anzeigen** laufen lassen — dieselben 12, die ihr in Phase 2 annotiert habt. Output → `predictions.jsonl` (eine Zeile pro Anzeige, JSON-Objekt mit `refnr` + den Schema-Feldern).

Erwartete Laufzeit: 40-60 s. Wenn deutlich länger: GPU geteilt? `nvidia-smi` checken.

**Run-Header in `notebooks/03_eval.ipynb`:** Predictions-Datei, Gold-Datei, Datum.

**Hypothese-Cell vor der Eval:** notiert, *welches Feld* ihr für am stärksten / am schwächsten haltet — und warum. Das ist der Anker, gegen den ihr gleich eure tatsächlichen Werte vergleicht.

**Per-Field-Accuracy berechnen:**

- Predictions und Gold per `refnr` joinen
- Pro Feld: Anteil der Anzeigen mit `pred == gold`
- Bei `skills_top3` ist *gleich* nicht offensichtlich: Set-Match (Reihenfolge egal) oder geordnete Liste? Trefft eine Entscheidung und begründet sie im Notebook
- Bei `gehalt_min_eur`: exakter Match oder mit Toleranz (z. B. ±5 %)? — auch eine eigene Entscheidung
- Wenn das Modell für eine Anzeige *kein valides JSON* liefert (kommt vor): zählt als Fail über alle Felder dieser Anzeige. Anzahl solcher Fälle separat festhalten — selbst ein Befund

**Tabelle im Notebook** — eine Zeile pro Feld (Feld, Accuracy, n_korrekt, n_total).

**Zwei schwächste Felder identifizieren** — die sind eure Iterations-Kandidaten für Phase 4. Pro schwachem Feld vermutet ihr eine Fehler-Klasse:

- **Schema-Problem** — der Wert ist im Text klar erkennbar, aber das Schema fängt ihn nicht sauber ab (Beispiel: "remote möglich nach Absprache" passt nicht eindeutig in `homeoffice ∈ {ja, teilweise, nein, nicht_genannt}`)
- **Modell-Problem** — der Wert ist im Text und schemakonform extrahierbar, aber das Modell wählt falsch (Beispiel: ignoriert "ab 50.000 €" und schreibt `nicht_genannt`)
- **Pipeline-Problem** — der Wert steht im Text, aber außerhalb des truncierten Kontexts oder durch Pre-Processing verloren

Begründet eure Vermutung **an konkreten Anzeigen** — schaut in 2-3 Fälle rein, an denen das Modell falsch lag. Was sagt der Text? Was hat das Modell extrahiert? Wo liegt die Lücke? Eine generische "wahrscheinlich Modellfehler"-Aussage ohne Anzeigen-Bezug ist nichts wert.

Diese Vermutung ist eure **Hypothese** für Phase 4 — dort manipuliert ihr genau den vermuteten Hebel und schaut, ob die Accuracy steigt.
