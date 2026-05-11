# Phase 2 — Schema challengen + Mini-Annotation

**Zeit:** 4 h
**Arbeitsform:** Paar-Annotation für κ-Vergleich (3 Paare aus 6 Schüler:innen) — jede:r annotiert für sich, der Vergleich zwischen euch ist der Lernhebel. Deliverable bleibt individuell.
**Was am Ende vorliegt:** `annotation/meine_gold.csv` mit 12 hand-annotierten Anzeigen + κ-Werte pro Feld + drei dokumentierte Edge Cases im Notebook `01_explore.ipynb`

---

## Lernziel

Annotieren ist ein eigener Skill — kein "Drumherum", sondern FIDP-Kerntätigkeit. Ihr erlebt am eigenen Material, wie viel Disziplin nötig ist, damit zwei Personen *denselben Text* auf *denselben Wert* abbilden — und was passiert, wenn das nicht klappt.

---

## Block 2.1 — Schema challengen (0,5 h)

Der Lehrer stellt das Schema vor (`SCHEMA.md` im Repo): 6 Felder mit Negativ-Definitionen.

Eure Aufgabe: das Schema **challengen**, *bevor* ihr damit annotiert.

- Geht eine Anzeige aus eurem Korpus durch und fragt: ließe sich jedes Feld eindeutig befüllen? Wo seid ihr unsicher?
- Sammelt 2-3 Edge Cases — Stellen, an denen die Anzeige zwischen zwei Werten schwebt
- Diskutiert in der Klasse: was würde man präzisieren, wenn man das Schema ändern könnte?

Wichtig: das Schema bleibt für die LS **fix**. Diese Diskussion ist ein Erfahrungs-Anker — Schemata sind in Wirklichkeit verhandelbar, nur in dieser LS nicht.

---

## Block 2.2 — Paar-Annotation, 12 Anzeigen (2,5 h)

**Setup:** 6 Schüler:innen → 3 Paare. Pro Paar:

- Einigt euch auf **12 gemeinsame Anzeigen** — z. B. aus dem Schnitt eurer beiden Phase-1-Korpora, oder aus einem der beiden, falls der Schnitt zu klein ist. Achtet auf einen Mix (verschiedene Suchanfragen, nicht nur eine Sorte).
- Annotiert **alleine, ohne mit der Partner:in zu sprechen** — jede:r in die eigene `annotation/meine_gold.csv`
- Am Ende der Phase tauscht ihr die CSVs — die Partner-CSV legt ihr als `annotation/partner_gold.csv` ab

(Ohne identische Anzeigen-IDs ist κ später nicht rechenbar — drauf achten.)

Während ihr annotiert:
- `skills_top3` mit `|` als Separator: `python|sql|excel`
- `notiz`-Spalte für Edge Cases nutzen — alles, was nicht eindeutig ins Schema passt

`nicht_genannt` ist **keine Sicherheits-Antwort bei Unsicherheit** — wählt es nur, wenn die Anzeige tatsächlich keine Aussage zum Feld macht. Wenn ihr unsicher seid, was im Text *gerade so* steht: das ist Material für 2.3.

**Halbzeit-Pause** (nach 6 Anzeigen): kurz innehalten. Wieviel Prozent eurer Annotationen sind `nicht_genannt`? Wenn auffällig viel, mit Lehrer ad hoc reden — vor allen 12 denselben Fehler zu machen lohnt nicht.

Werkzeug: `validate.py` prüft Schema-Konformität. Lauft es zwischendurch — Tippfehler oder ungültige Werte sind so früh sichtbar:

```bash
python annotation/validate.py annotation/meine_gold.csv
```

---

## Block 2.3 — κ rechnen + Edge Cases dokumentieren (1 h)

```bash
python annotation/validate.py annotation/meine_gold.csv --kappa-against annotation/partner_gold.csv
```

(Falls `validate.py` Schema-Verletzungen meldet — erst korrigieren, dann κ rechnen. Beides muss laufen.)

In `notebooks/01_explore.ipynb` ergänzt ihr eine Markdown-Zelle:

| Feld | κ (n=12) | Disagreement-Beispiele (Anzeigen-IDs) |
|---|---|---|
| ... | ... | ID + kurze Beschreibung |

Plus: aus eurer `notiz`-Spalte und den κ-Befunden formuliert ihr **drei Edge Cases** in eigenen Worten. Pro Edge Case:

- An welcher Anzeige ist er aufgetaucht?
- Welche zwei Lesarten standen zur Wahl?
- Welche Schema-Klärung würde ihn lösen — wenn das Schema offen wäre?

Cheatsheet zur κ-Interpretation: `CHEATSHEETS/kappa.md`.
