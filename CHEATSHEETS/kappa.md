# Cohen's κ — Cheatsheet

**Wann ihr das braucht:** Phase 2 (Mensch ↔ Mensch), Phase 5 (Mensch ↔ Frontier-LLM).

## Anschauung zuerst — bevor die Formel kommt

Stellt euch vor, ihr und eine Kollegin sortieren Bewerbungseingänge in zwei Stapel: *passt zur Stelle* / *passt nicht*. Am Ende vergleicht ihr eure Stapel und stellt fest: in 80 % der Fälle wart ihr einig.

Die naive Frage: *"80 % — ist das gut?"*

Die schärfere Frage: *"Wie viel davon hätten zwei Würfel-Werfer auch geschafft?"* Wenn 90 % aller Bewerbungen offensichtlich nicht zur Stelle passen und beide entsprechend in 90 % der Fälle "passt nicht" sagen, **erreichen sie rein zufällig schon 0,9² + 0,1² = 0,82, also 82 % Übereinstimmung — ohne hingeschaut zu haben**. Eure 80 % wären dann *schlechter als blindes Raten*.

κ ist genau das: **wie viel von eurer Übereinstimmung ist Können, wie viel ist Zufall?** 1 = perfekt, 0 = nicht besser als Zufall, negativ = schlechter als Zufall.

Das ist die berufliche Frage: *"Können wir uns auf unsere Annotation verlassen, oder reden wir uns Übereinstimmung schön?"*

## Formel

```
κ = (p_o − p_e) / (1 − p_e)

p_o = beobachtete Übereinstimmung    (Anteil identischer Labels)
p_e = erwartete Zufalls-Übereinstimmung
    = Σ über Klassen c: (Häufigkeit_A[c] / N) × (Häufigkeit_B[c] / N)
```

Wertebereich (Landis & Koch 1977 — die Tabelle, auf die alle verweisen):

| κ | Bedeutung |
|---|---|
| 1,00 | perfekt |
| 0,81 – 1,00 | fast perfekt |
| 0,61 – 0,80 | substanziell |
| 0,41 – 0,60 | moderat |
| 0,21 – 0,40 | mäßig |
| 0,00 – 0,20 | schlecht |
| < 0,00 | schlechter als Zufall |

## Rechenbeispiel von Hand

10 Anzeigen, Feld `vertragsart`. A und B annotieren parallel:

| ID | A | B | Übereinst.? |
|---|---|---|---|
| 1 | ausb | ausb | ✓ |
| 2 | ausb | fest | ✗ |
| 3 | fest | fest | ✓ |
| 4 | ausb | ausb | ✓ |
| 5 | ausb | ausb | ✓ |
| 6 | fest | ausb | ✗ |
| 7 | ausb | ausb | ✓ |
| 8 | ausb | ausb | ✓ |
| 9 | ausb | ausb | ✓ |
| 10 | fest | fest | ✓ |

Schritt 1 — beobachtete Übereinstimmung:

```
p_o = 8/10 = 0,80
```

Schritt 2 — erwartete Zufalls-Übereinstimmung. Klassen-Häufigkeit pro Person:

```
A: ausb=7/10=0,7   fest=3/10=0,3
B: ausb=8/10=0,8   fest=2/10=0,2

p_e = (0,7 × 0,8) + (0,3 × 0,2) = 0,56 + 0,06 = 0,62
```

Schritt 3 — κ:

```
κ = (0,80 − 0,62) / (1 − 0,62) = 0,18 / 0,38 = 0,474
```

**Pointe:** 80 % Übereinstimmung sieht gut aus, aber κ = 0,47 heißt nur **moderat**. Bei der schiefen 70/30-Verteilung produziert reines Raten schon 62 % Übereinstimmung — eure echte Leistung ist nur die Differenz darüber.

## Mit `validate.py` rechnen

```bash
python annotation/validate.py annotation/meine_gold.csv \
       --kappa-against annotation/partner_gold.csv
```

Output ungefähr:

```
Cohen's kappa: meine_gold.csv vs. partner_gold.csv
Gemeinsame IDs: 12

Feld                    kappa   Übereinst.
------------------------------------------
homeoffice              0,621        75 %
vertragsart             1,000       100 %
erfahrungslevel         0,474        80 %
```

Das Skript rechnet κ **pro kategorialem Feld einzeln** — eine Gesamt-Zahl gibt es nicht, Schema-Felder verhalten sich unterschiedlich.

**Edge-Case:** wenn alle dieselbe Klasse für ein Feld wählen (z. B. alle 12 sind `vertragsart=ausbildung`), ist `p_e = 1,0` und κ ist mathematisch **undefiniert** (Division durch 0). `validate.py` returnt `nan` — das ist gewollt. Berichtet ehrlich: *"κ ist nan, weil keine Variation in der Klassenwahl auftrat — die Übereinstimmung ist perfekt, aber κ ist hier nicht identifizierbar."*

## Häufige Fallen

**Falle 1 — kleines n macht κ instabil.** Bei 12 Anzeigen schwankt κ deutlich. Ein einziger Fehl-Match kann κ um 0,1 verschieben. Berichtet immer Wert + Stichprobengröße. Wer im Fachgespräch nach Konfidenz gefragt wird, antwortet ehrlich: *"bei n = 12 ist κ = 0,62 nahezu kompatibel mit 0,50 oder 0,75 — die Stichprobe ist zu klein für scharfe Aussagen."*

**Falle 2 — Kappa-Paradox bei extrem unbalancierten Klassen.** Wenn 11 von 12 Anzeigen `ausbildung` sind, ist `p_e` sehr hoch (Zufall trifft fast immer), und selbst hohe Übereinstimmung erzeugt niedrige κ-Werte. Gute Annotation, "schlechtes" κ. Bei `gehalt_zeitraum` (oft `null`) kann das greifen.

**Falle 3 — κ misst Konsistenz, nicht Wahrheit.** Zwei Annotator:innen können sich einig und beide falsch sein. Für Wahrheit braucht ihr ein **Gold** — z. B. den Frontier-LLM-Vergleich aus Phase 5 oder eine Lehrer-Adjudication.

Daraus folgt eine wichtige Unterscheidung:

- **κ Mensch ↔ Mensch** (Phase 2) zeigt, wie *konsistent* euer Schema ist
- **κ Mensch ↔ Frontier-LLM** (Phase 5) zeigt, ob das Frontier nahe genug an menschlicher Annotation ist, um als Annotator-Ersatz zu taugen

Beide heißen "κ", messen aber inhaltlich unterschiedliche Dinge.

## Welche κ-Variante in welchem Fall?

| Variante | Wann | Bei euch? |
|---|---|---|
| **Cohen's κ** | 2 Annotator:innen, kategoriale Werte | **Ja** — `validate.py --kappa-against` |
| Fleiss' κ | 3+ Annotator:innen | nein (immer paarweise) |
| Quadratic Weighted κ (QWK) | ordinale Werte, Abstand zwischen Levels zählt | streng genommen für `erfahrungslevel` korrekt — wir verwenden trotzdem Cohen's κ, weil im Korpus `junior` und `senior` dominieren und der ordinale Vorteil klein bleibt |

## Number-Receipt-Form für Notebook + Fachgespräch

> *"Mein Inter-Annotator-κ auf Feld `erfahrungslevel` (n=12) ist 0,62 — substanziell. Die zwei Disagreement-Fälle waren beide bei *Werkstudent vs. Praktikum* — Schema-Edge-Case, in den drei Edge Cases aus Phase 2 dokumentiert."*

Wert + Stichprobe + Disagreement-Klassifikation + Implikation. Ohne diese vier Bestandteile wirkt das κ wie eine Buzzword-Zahl.
