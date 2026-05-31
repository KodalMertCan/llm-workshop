# Make-or-Buy: Sollen die restlichen Anzeigen vom Frontier-LLM annotiert werden?

**Stand:** 2026-05-18  
**Stichproben-Basis:** 12 hand-annotierte Anzeigen aus Phase 2, davon 9 für den Mensch↔Frontier-Vergleich (3 als Few-Shot-Beispiele ausgeschlossen)

## Empfehlung

Ich empfehle einen **Hybrid-Ansatz**: die restlichen ~60 Anzeigen werden vom Frontier-LLM (GPT-5.5 oder Claude Opus) annotiert, und ein Mensch reviewt eine **20%-Stichprobe** der vom Frontier produzierten Annotationen. Die Annotation selbst macht das Frontier, die Qualitätssicherung bleibt beim Menschen.

Die reine Mensch-Annotation aller 60 Anzeigen wäre zwar methodisch am sichersten, kostet aber bei realistisch 8-10 Minuten pro Anzeige rund 9 Stunden Arbeitszeit gegenüber wenigen Minuten Frontier-Inferenz plus einer Stunde Mensch-Review. Reine Frontier-Annotation ohne Mensch-Review wäre auf Basis meiner κ-Werte zwar fast tragfähig, aber gerade bei den schwierigen Edge-Cases (siehe unten) müsste ich erst sichtbar machen können, wenn der Frontier falsch liegt. Das geht nur mit Mensch-Review.

## Begründung an meinen κ-Werten

Cohen's κ zwischen meiner Hand-Annotation und der ChatGPT-Annotation auf den 9 nicht-Few-Shot-Anzeigen ist sehr stark: 1.0 auf `vertragsart`, 0.84 auf `erfahrungslevel`, 0.77 auf `homeoffice`. Bei `vertragsart` haben Mensch und Frontier exakt identisch geantwortet, weil die textuellen Marker eindeutig sind ("Ausbildung" steht oder steht nicht). Hier kann ich dem Frontier blind vertrauen. Bei `homeoffice` und `erfahrungslevel` liegen die beiden Disagreements auf derselben Anzeige (Lantenhammer) und betreffen genau den Edge Case, den ich schon in Phase 2 mit der Partner-Annotation als Schema-Lücke identifiziert hatte: "Home Office möglich" ohne Tagesangabe und "2-3 Jahre Berufserfahrung mit Führungsaufgaben" sind keine Frontier-Fehler, sondern unterspezifizierte Schema-Definitionen. Das Frontier hat sich strikter ans Schema gehalten als ich selbst — interessanterweise insbesondere bei `skills_top3`, wo ChatGPT die eigene Schema-Regel "keine Methoden" konsequenter befolgt als ich.

Bei den nicht-kategorialen Feldern (`gehalt_min_eur`, `gehalt_zeitraum`, `skills_top3` als Set) ist die Übereinstimmung ebenfalls sehr hoch. Skills-Disagreements (7 von 9 Anzeigen) sind fast alle entweder Reihenfolge-Unterschiede oder verschiedene-aber-gleich-valide Top-3-Auswahlen aus dem gleichen Pool. Echte semantische Disagreements gibt es höchstens bei 2-3 Anzeigen.

## Schwellwert-Logik

Meine Grenze für reines Buy ohne Mensch-Review wäre κ ≥ 0.85 auf allen kategorialen Feldern und ein gut definiertes Schema ohne offene Edge Cases. Bei mir ist `vertragsart` über der Schwelle, `erfahrungslevel` knapp dran, `homeoffice` darunter. Außerdem habe ich aus Phase 2 drei dokumentierte Schema-Lücken (alle bei `erfahrungslevel`), die in der Phase-5-Auswertung erneut aufgetaucht sind. Das heißt: solange das Schema diese Edge Cases nicht eindeutig auflöst, würde reines Frontier-Annotieren systematisch dieselben Fälle falsch entscheiden — nur eben konsistent falsch statt zufällig falsch. Das ist methodisch noch schlechter als menschliche Inkonsistenz.

Was müsste anders sein, damit ich auf reines Buy umstelle? Erstens: die drei Schema-Lücken bei `erfahrungslevel` mit klaren Regeln auflösen (ein zusätzlicher Wert für "Erfahrung erwähnt aber ohne Zahl/Titel" oder eine explizite Tie-Breaker-Regel). Zweitens: die Stichprobengröße auf ≥30 Anzeigen erhöhen, damit κ-Werte stabil interpretierbar sind. Bei n=9 schiebt eine einzelne Anzeige den Wert um 0.15 Punkte — das ist statistisch fragil.

## Risiko-Sicherung

Was geht schief, wenn meine Empfehlung falsch ist? Drei Hauptrisiken: erstens, dass das Frontier bei Gehaltsangaben systematisch null schreibt, wo eine konkrete Zahl im Text steht (in meiner Phase-3-Iteration B war das ein neu entstandenes Modell-Problem) — Fehler hier sind gravierend, weil sie Filtersuchen verfälschen. Zweitens, dass `homeoffice`-Werte zwischen `ja` und `teilweise` systematisch verrutschen — relevant für Bewerber:innen, die nach echtem Hybrid suchen. Drittens, dass `skills_top3` zwar formal korrekt sind, aber andere Skills wählen als ein Branchenexperte priorisieren würde.

Die konkrete Stichproben-Kontrolle: Aus jedem 5er-Block der vom Frontier annotierten Anzeigen wähle ich eine zufällig aus, annotiere sie nochmal selbst und vergleiche. Bei mehr als 1 substanziellem Disagreement pro 5er-Block (also <80% Übereinstimmung) wird der gesamte Block menschlich re-annotiert und der Prompt wird angepasst. Zusätzlich läuft auf 100% der Frontier-Outputs der `validate.py`-Schema-Check — Schema-Verletzungen führen automatisch zur Re-Annotation der betroffenen Anzeige. So fange ich sowohl harte Schema-Fehler (über Validator) als auch weiche Interpretations-Fehler (über Stichprobe) ab, ohne den Großteil der Kosten zu opfern.

Bei einem hypothetischen produktiven Einsatz mit echten Bewerber:innen würde ich zusätzlich einen Confidence-Score pro Frontier-Antwort einfordern und alle Anzeigen unter z.B. 0.7 Confidence komplett dem Mensch geben. Aktuell gibt mir die ChatGPT-Web-Schnittstelle diesen Score nicht, das wäre ein Grund, auf API-Zugriff umzustellen — für n=60 Anzeigen rechtfertigen die Kosten den Aufwand aber nicht.