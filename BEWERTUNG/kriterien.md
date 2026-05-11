# Bewertungs-Kriterien

Drei Bereiche, je vier Stufen. Eure Note ergibt sich aus dem gewichteten Mittel — sofern keiner der Mindeststandards greift (siehe Ende).

| Bereich | Gewicht | Worauf gerichtet |
|---|---|---|
| **1 — Pipeline & Methodik** | 40 % | Lauffähige Pipeline, korrekte Eval, dokumentierte Iterationen, schemakonforme Mini-Gold-CSV, korrekte κ-Berechnung |
| **2 — Reflexion & Diagnose** | 30 % | Schema-/Modell-/Pipeline-Trennung an eigenen Daten, Bias am eigenen Korpus, Make-or-Buy-Begründung, 3B-Halluzinations-Klassen |
| **3 — Fachgespräch** | 30 % | Verteidigung der eigenen Zahlen-Belege, Berufstransfer, Follow-up-Fragen |

**Stufen-Logik (gilt überall):**

- **Stufe 4** — über Standard hinaus: eigene Verbindung zwischen Daten und Schluss, methodische Selbstkritik, zusätzlich gewählte Hebel
- **Stufe 3** — Standard sauber erfüllt: alles da, korrekt, aber nichts darüber hinaus
- **Stufe 2** — Lücken oder Generik: vorhanden aber unbelegt, oder Pflicht-Bestandteile fehlen
- **Stufe 1** — fehlt, abgeschrieben oder nicht eigenständig

---

## 1. Pipeline & Methodik (40 %)

| Stufe | Verhalten |
|---|---|
| **4** | Pipeline reproduzierbar, 2+ Iterationen mit Hypothese / Aktion / Δ / Diagnose, **plus etwas darüber hinaus**: dritte Iteration, eigene Metrik (z. B. JSON-Parse-Failure-Rate als separater Indikator), eigener Validator-Schritt für die Skalierung, oder explizit dokumentierte Match-Logik für Edge-Fälle mit Begründung (z. B. Toleranz-Regel für `gehalt_min_eur`) |
| **3** | Pipeline läuft reproduzierbar (Run-Header mit Modell, GPU, Datum), Per-Field-Accuracy berechnet mit dokumentierten Match-Entscheidungen für `skills_top3` und `gehalt_min_eur`, 2 Iterationen mit Hypothese- und Auswertung-Cell, κ schemakonform berechnet, Mini-Gold-CSV ohne `validate.py`-Verstöße |
| **2** | Pipeline läuft, aber Eval ist lückig — z. B. Iterations-Tabelle ohne Hypothese-Spalte, κ-Wert ohne Disagreement-Liste, Match-Entscheidungen für skills/gehalt nicht dokumentiert, oder JSON-Parse-Fails ignoriert |
| **1** | Keine eigene Pipeline-Inferenz (siehe Mindeststandard), Iterationen nur hypothetisch ("hätte ich gemacht"), oder CSVs nicht schemakonform |

---

## 2. Reflexion & Diagnose (30 %)

| Stufe | Verhalten |
|---|---|
| **4** | Schema-/Modell-/Pipeline-Trennung mit **konkreten Anzeigen-IDs** als Beleg, eigene Schwellwert-Logik (z. B. Signal-vs-Rausch-Argument bei n=12: *"ab 2 Anzeigen Differenz nehme ich es ernst"*), Make-or-Buy-Memo mit konkretem κ-Schwellwert + Risiko-Sicherung, 3B-Halluzinations-Klassen mit **Mechanismus-Hypothese** (warum genau dieses Muster, nicht nur "ist anders") |
| **3** | Alle vier Reflexionen vorhanden (Bias-Notiz Phase 1, Iterations-Diagnose Phase 4, Make-or-Buy Phase 5, 3B-Klassen Phase 6), substantiell, an konkreten Anzeigen belegt. Schema-/Modell-/Pipeline-Trennung sauber — aber ohne eigene Schwellwert-Logik oder methodische Selbstkritik |
| **2** | Reflexionen vorhanden, aber generisch — ohne konkrete Anzeigen-IDs, ohne Schema-/Modell-/Pipeline-Trennung. Make-or-Buy ohne eigenen κ-Bezug ("kommt drauf an"). Bias als Aufzählung von Kategorien ohne Befund am eigenen Korpus |
| **1** | Reflexionen fehlen, sind bei mehreren Schüler:innen identisch (= abgeschrieben), oder ohne Bezug zu eigenen Daten |

---

## 3. Fachgespräch (30 %)

10 min Einzelgespräch mit dem Lehrer am Ende der LS. Vier Fragen-Kategorien:

1. **Iterations-Diagnose** — was hat warum geholfen? Schema-/Modell-/Pipeline-Trennung an eigenen Daten
2. **Frontier-Make-or-Buy** — eigene κ-Werte, eigene Begründung
3. **Modellgrößen-Wahl** — 3B-Halluzinations-Klassen
4. **Berufstransfer** — wie sähe sowas im eigenen Ausbildungsbetrieb aus?

| Stufe | Verhalten |
|---|---|
| **4** | Erklärt eigene Zahlen (κ, Δ, Accuracy) **flüssig im Sinnzusammenhang, nicht abgelesen**. Berufstransfer mit **konkretem Beispiel** *oder* **begründeter Hypothese**, wo so etwas im eigenen Betrieb passen würde. Beantwortet Follow-up-Fragen souverän, gibt eigene Schwächen ehrlich zu (statt zu verteidigen). |
| **3** | Erklärt eigene Zahlen mit kurzem Notebook-Blick zur Orientierung. Berufstransfer benannt aber generisch ("könnte man bestimmt verwenden"). Follow-up-Fragen werden bestanden. |
| **2** | Eigene Zahlen werden **vorgelesen** statt erklärt — die Bedeutung kommt nicht mit. Berufstransfer fehlt oder bleibt vage. Follow-ups werden teils nicht beantwortet — aber eigene Inhalte sind erkennbar. |
| **1** | Weiß nicht, welche eigenen Zahlen im Notebook stehen, kann eigene Iterationen nicht zuordnen, weicht systematisch aus. |

---

## Mindeststandards (überschreiben das gewichtete Mittel)

- **Fachgespräch < Stufe 2** (kann eigene Inhalte nicht erklären) → max. *ausreichend* in der Gesamtnote (KI-Resistenz-Anker — wer die eigenen Zahlen aus dem Notebook nicht verteidigen kann, hat das Hauptlernziel verfehlt)
- **Pipeline läuft nicht** (keine eigene Inferenz) → max. *befriedigend* in der Gesamtnote

Beide Standards greifen unabhängig. Wer Pipeline fehlt *und* Fachgespräch durchfällt: niedrigerer Cap zählt.
