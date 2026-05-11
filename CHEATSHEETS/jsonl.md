# JSONL — Cheatsheet

**Wann ihr das braucht:** ab Phase 1 — euer Korpus liegt als `daten/eigener_korpus.jsonl`. Auch Modell-Predictions speichern wir später so.

## Was ist JSONL?

**JSONL = JSON Lines.** Pro Zeile ein eigenständiges JSON-Objekt, getrennt durch Newlines. Kein Array drumherum, keine Kommas zwischen den Zeilen.

```jsonl
{"refnr": "10000-1234", "titel": "Fachinformatiker DPA", "firma": "Acme GmbH", "text": "Wir suchen..."}
{"refnr": "10000-5678", "titel": "Datenanalyst", "firma": "Beta AG", "text": "Zur Verstärkung..."}
{"refnr": "10000-9012", "titel": "BI-Entwickler", "firma": "Gamma KG", "text": "..."}
```

Verglichen mit klassischem JSON wäre dasselbe:

```json
[
  {"refnr": "10000-1234", "titel": "Fachinformatiker DPA", ...},
  {"refnr": "10000-5678", "titel": "Datenanalyst", ...},
  {"refnr": "10000-9012", "titel": "BI-Entwickler", ...}
]
```

## Warum JSONL statt JSON?

| | JSON-Array | JSONL |
|---|---|---|
| **Streamen** | Parser braucht ganze Datei | Zeile für Zeile lesbar |
| **Anhängen** | Datei neu schreiben | Einfach `>>` ans Ende |
| **Eine Zeile defekt** | Ganze Datei kaputt | Restliche Zeilen funktionieren |
| **Speicher bei großen Dateien** | Komplettes Array im RAM | Eine Zeile reicht |
| **`grep` / `wc -l` / `head`** | Sinnlos | Zählt Datensätze, zeigt erste N |

Konkret bei euch: euer Korpus wächst inkrementell beim Scrapen — jede neue Anzeige kommt einfach unten dran. Predictions später ähnlich: pro Eingangs-Anzeige eine Output-Zeile.

## In Python schreiben

```python
import json

anzeigen = [
    {"refnr": "10000-1234", "titel": "Fachinformatiker DPA", "text": "..."},
    {"refnr": "10000-5678", "titel": "Datenanalyst", "text": "..."},
]

with open("daten/eigener_korpus.jsonl", "w", encoding="utf-8") as f:
    for anzeige in anzeigen:
        f.write(json.dumps(anzeige, ensure_ascii=False) + "\n")
```

**`ensure_ascii=False`** ist wichtig — sonst werden Umlaute zu `ä` o.ä. Lesbar bleibt's nur ohne.

**Anhängen** statt überschreiben: `open(..., "a", ...)` — nützlich, wenn ihr in Schleifen scrape und nach jeder Anzeige direkt schreibt (so verliert ihr bei einem Crash nicht alles).

## In Python lesen

```python
import json

with open("daten/eigener_korpus.jsonl", "r", encoding="utf-8") as f:
    anzeigen = [json.loads(line) for line in f]

print(f"{len(anzeigen)} Anzeigen geladen")
print(anzeigen[0]["titel"])
```

Streaming-Variante (groß, RAM-schonend):

```python
with open("daten/eigener_korpus.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        anzeige = json.loads(line)
        # ... pro Anzeige verarbeiten
```

## Mit pandas

```python
import pandas as pd

df = pd.read_json("daten/eigener_korpus.jsonl", lines=True)   # Lesen
df.to_json("daten/eigener_korpus.jsonl", orient="records", lines=True, force_ascii=False)  # Schreiben
```

Praktisch für Phase 1.2 (Korpus inspizieren — Längen-Verteilung, Häufigkeiten).

## Häufige Fallen

- **Newlines im Text-Feld:** Eine JSON-Zeile darf intern keine echten Newlines enthalten. `json.dumps` kümmert sich darum (escaped `\n`) — sorgt aber selbst dafür, falls ihr Strings manuell zusammenbaut.
- **Letzte Zeile ohne `\n`:** Manche Parser stolpern darüber. `json.dumps(...) + "\n"` immer schreiben, auch beim letzten Datensatz.
- **`json.load` vs. `json.loads`:** `load` liest die *ganze Datei* als ein JSON-Dokument — bei JSONL knallt das. Nutzt `json.loads` (mit s = string) pro Zeile.
- **Excel öffnet `.jsonl` nicht direkt:** Zum Reinschauen `head daten/eigener_korpus.jsonl` im Terminal oder `pd.read_json(..., lines=True).head()` im Notebook.

## Quick-Check

```bash
wc -l daten/eigener_korpus.jsonl       # Anzahl Anzeigen
head -1 daten/eigener_korpus.jsonl     # erste Anzeige sehen
head -1 daten/eigener_korpus.jsonl | python -m json.tool   # erste Anzeige lesbar formatieren
```
