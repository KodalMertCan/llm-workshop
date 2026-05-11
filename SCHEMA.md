# SCHEMA — Kanonische Felder & Negativ-Definitionen

Dieses Schema ist **fix für die LS** (siehe Phase 2.1). Ihr annotiert eure 12 Anzeigen gegen diese 6 Felder, und eure Pipeline extrahiert genau diese 6 Felder. Diskussion und Challenge in 2.1 sind explizit erwünscht — das Ergebnis ändert das Schema aber nicht, sondern liefert Material für eure Disagreement-Liste.

## Überblick

| Feld | Datentyp |
|---|---|
| `homeoffice` | kategorial (5 Werte) |
| `vertragsart` | kategorial (5 Werte) |
| `erfahrungslevel` | kategorial (5 Werte) |
| `gehalt_min_eur` | int oder `null` |
| `gehalt_zeitraum` | kategorial (3 Werte) |
| `skills_top3` | Liste (max. 3 Strings) |

Pro Anzeige in eurer `meine_gold.csv` eine Zeile mit einem Wert pro Feld.

---

## `homeoffice`

**Erlaubte Werte:** `ja`, `teilweise`, `nein`, `remote`, `nicht_genannt`

- `remote` — 100 % Homeoffice, *ortsunabhängig*. Erkennbar an "Vollzeit Remote", "100 % Home-Office", "Deutschland-weit von zu Hause".
- `teilweise` — Hybrid. Mischung aus Büro und Homeoffice. Formulierungen: "Hybrid", "anteilig Homeoffice", "mobiles Arbeiten möglich", "2 Tage pro Woche Homeoffice".
- `ja` — Homeoffice angeboten, Modus unspezifisch (weder klar remote noch eindeutig hybrid). In der Praxis selten.
- `nein` — explizite Präsenzpflicht, kein Homeoffice.
- `nicht_genannt` — die Anzeige sagt zum Thema Homeoffice gar nichts.

**Faustregel `nicht_genannt`:** wählt ihr **nur**, wenn die Anzeige tatsächlich keine Aussage macht — *nicht* als Sicherheits-Antwort bei Unsicherheit.

---

## `vertragsart`

**Erlaubte Werte:** `ausbildung`, `festanstellung`, `praktikum`, `werkstudent`, `sonstiges`

- `ausbildung` — duale Berufsausbildung (üblicherweise 3 Jahre)
- `festanstellung` — unbefristeter oder befristeter Vertrag in regulärem Arbeitsverhältnis (auch Senior-Positionen)
- `praktikum` — befristetes Praktikum im Rahmen eines Studiums oder als Schul-Praktikum
- `werkstudent` — Werkstudenten-Vertrag während eines Studiums
- `sonstiges` — alles andere (Freelance, Leiharbeit, Trainee-Programme, …) oder nicht eindeutig klassifizierbar

**Hinweis:** Trainee-Programme sind Edge Case — meist `festanstellung`, manchmal `sonstiges`. Eure Entscheidung in der `notiz`-Spalte begründen.

---

## `erfahrungslevel`

**Erlaubte Werte:** `junior`, `mid`, `senior`, `egal`, `nicht_genannt`

- `junior` — Berufseinsteiger, ≤2 Jahre Berufserfahrung erforderlich. **`ausbildung` zählt immer als `junior`.**
- `mid` — mittlere Erfahrung, ~2–5 Jahre. Erkennbar an "Erfahrung erforderlich" ohne explizit "Senior".
- `senior` — Senior-Position, ≥5 Jahre Erfahrung. Erkennbar an Titel ("Senior X") oder konkreten Anforderungen ("8+ Jahre").
- `egal` — die Anzeige akzeptiert explizit jedes Level ("Junior bis Senior willkommen").
- `nicht_genannt` — keine Aussage zum Erfahrungslevel.

**Hinweis:** Werkstudenten und Praktika sind Edge Case — weder offensichtlich `junior` (sind ja noch Studierende), noch klar `nicht_genannt`. Eure Entscheidung dokumentieren.

---

## `gehalt_min_eur`

**Datentyp:** ganze Zahl (int) oder `null`.

**Bedeutung:** das **Mindestgehalt**, das in der Anzeige explizit genannt ist — als ganze Zahl, ohne Komma oder Tausender-Trennung.

- `null` — kein konkretes Gehalt genannt. Auch bei "nach Vereinbarung", "marktüblich", "attraktive Vergütung", oder Platzhalter wie "XX.XXX EUR".
- **Konkrete Zahl** — bei Range "ab 50.000 €" oder "50.000–60.000 €" nehmt ihr die *untere Grenze* (`50000`).

**Hinweis:** Tarif-Ausbildungen ("Ausbildungsvergütung nach Tarif") sind ohne konkrete Zahl `null`, auch wenn jeder weiß, dass es einen Tarif gibt.

---

## `gehalt_zeitraum`

**Erlaubte Werte:** `monat`, `jahr`, `null`

**Bedeutung:** zu welchem Zeitraum die Zahl in `gehalt_min_eur` gehört.

- `monat` — Monatsgehalt (typisch bei Ausbildungen, Praktika, Werkstudent)
- `jahr` — Jahresgehalt (typisch bei Festanstellungen)
- `null` — kein Zeitraum nennbar, weil `gehalt_min_eur` selbst `null` ist

**Konsistenz-Regel:** wenn `gehalt_min_eur` null ist, *muss* `gehalt_zeitraum` auch null sein. Sonst meldet `validate.py`.

---

## `skills_top3`

**Datentyp:** Liste mit maximal 3 Strings (kann auch leer sein).

**Bedeutung:** die im Text **explizit genannten** technischen Skills / Tools — bis zu drei, in der Reihenfolge, wie sie für die ausgeschriebene Stelle relevant erscheinen.

**Was rein darf:**
- Programmiersprachen: `Python`, `SQL`, `Java`, `JavaScript`, …
- Tools / Plattformen: `Power BI`, `Tableau`, `Excel`, `Snowflake`, `Databricks`, `dbt`, `AWS`, `Azure`, …
- Frameworks / Libraries: `React`, `Pandas`, `TensorFlow`, …
- Methodische technische Skills: `Machine Learning`, `ETL`, `Datenmodellierung`

**Was NICHT rein darf:**
- Soft Skills: `Teamfähigkeit`, `Kommunikationsfähigkeit`, `eigenständiges Arbeiten`
- Sprachen: `Deutsch`, `Englisch`
- Schulfächer / formale Qualifikationen: `Mathematik`, `Abitur`, `Realschulabschluss`
- Generische Fachgebiete: `Informatik`, `BWL`

**Format-Konvention in der CSV:** mit Pipe `|` getrennt, z. B. `python|sql|excel`.

**Faustregel:** wenn ihr unsicher seid, ob ein Begriff "technisch" genug ist — fragt euch, ob die Bewerber:in *konkretes Werkzeug-Wissen* mitbringt. `Python` ja, `Mathematik` nein.

---

## Was hier *nicht* steht — und das ist Absicht

Es gibt Stellen in Stellenanzeigen, an denen die obigen Definitionen nicht ausreichen — die *eindeutige* Zuordnung schwebt zwischen zwei Werten. Beispiele:

- "ab dem 2. Ausbildungsjahr Homeoffice möglich" — welcher Wert für `homeoffice`?
- "Werkstudent (m/w/d)" — welcher Wert für `erfahrungslevel`?
- "Praktikumsentschädigung 800 €" — `monat` oder `jahr`?

Diese Sorte Lücke ist genau das Material für eure **drei Edge Cases** in Phase 2.3 — findet eure am eigenen Korpus und dokumentiert sie im Notebook.
