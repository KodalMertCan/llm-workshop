# Git-Grundlagen — Cheatsheet

**Wann ihr das braucht:** durchgängig — euer Repo ist die Phasen-Abgabe.

## Setup

Ihr habt das Template-Repo zum eigenen Repo gemacht ("Use this template" auf GitHub). Klont es **einmalig im Jupyterhub-Terminal** (nicht lokal — der Code lebt auf dem Server, das Home ist zwischen gauss + euler synchronisiert):

```bash
# Im Jupyterhub-Terminal
cd ~                                                       # /home/jovyan
git clone https://github.com/<euer-username>/ls-information-extraction.git
cd ls-information-extraction
```

> **SSH geht im Schulnetz nicht** (Port 22 ist gesperrt). Deshalb läuft alles über HTTPS + Personal Access Token.

### Personal Access Token einmalig anlegen

GitHub fragt beim ersten `git push` (und je nach Konfiguration schon beim Clone) nach Username + Passwort. Als Passwort braucht ihr ein **Personal Access Token** — ein normales GitHub-Passwort wird seit 2021 nicht mehr akzeptiert.

1. GitHub im Browser → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **"Generate new token (classic)"**
2. Scope: **`repo`** aktivieren (lesen + schreiben für eure eigenen Repos)
3. Expiration: 90 Tage reichen für die LS — oder „no expiration", wenn ihr's einfach haben wollt
4. Token wird **einmal** angezeigt — kopieren und sicher merken (Passwort-Manager). Geht der verloren: neuer Token, kein Wiederherstellen.

Beim ersten `git push`:
- **Username:** euer GitHub-Login
- **Password:** der Token (NICHT euer GitHub-Passwort)

Git cached den Token im Container für die laufende Session. Den Token **niemals** in Notebooks oder Code committen — wenn er versehentlich pusht, sofort auf GitHub revoken und neu erstellen.

## Daily Workflow

Vor jeder Sitzung — letzten Stand holen:

```bash
cd ~/ls-information-extraction
git pull
```

Während der Sitzung — Notebooks und Markdown-Dateien im Jupyterhub bearbeiten.

Am Ende jeder Phase — Stand sichern:

```bash
git add notebooks/02_extract.ipynb annotation/meine_gold.csv
git commit -m "Phase 2: 12 Anzeigen annotiert, κ + Edge Cases"
git push
```

**Commit-Messages — Faustregel:**
- Phase und Inhalt nennen
- Bei Eval-Zwischenständen Zahlen in den Commit-Body packen, z. B.:

```
Phase 4 Iteration A: Schema-Klarstellung homeoffice

Δ homeoffice: 67 % → 92 % (+25 Pt)
Andere Felder unverändert.
```

Diese Zahlen-Belege sind später beim Fachgespräch eure Erinnerungs-Quelle.

## Was kommt rein, was nicht

`.gitignore` ist eingerichtet. Schaut rein.

**Rein:**
- `notebooks/*.ipynb` (eure ausgefüllten Notebooks)
- `annotation/meine_gold.csv` + `annotation/partner_gold.csv` + `annotation/frontier_gold.csv`
- `daten/eigener_korpus.jsonl` (euer Korpus aus Phase 1)
- `memo_make_or_buy.md` (Phase 5)
- Markdown-Reflexionen, falls außerhalb der Notebooks

**Nicht:**
- `predictions_*.jsonl` (zu groß, in `.gitignore`)
- `__pycache__/` (Python-Cache, in `.gitignore`)
- API-Keys oder Login-Daten (NIE)
- Modell-Checkpoints (mehrere GB)

## Branches — braucht ihr nicht zwingend

Ein einziger `main`-Branch reicht. Ihr arbeitet alleine an eurem Repo, niemand anderes pusht hinein.

**Optional, wenn ihr üben wollt:** ein Branch pro Phase.

```bash
git checkout -b phase-4-iteration
# arbeiten, committen
git push -u origin phase-4-iteration
# am Ende: PR auf main, selbst mergen
```

Übt den Berufstransfer (Branches + PRs sind Standard), kostet aber Zeit. Empfehlung: einmal pro Phase ein Commit auf `main` reicht — Zeit lieber in Reflexion stecken.

## Häufige Probleme

### `git push` wird abgelehnt

```
! [rejected] main -> main (fetch first)
```

Jemand (oder ein anderer Computer von euch) hat zwischendurch gepusht. Erst pullen, dann pushen:

```bash
git pull --rebase
git push
```

### Merge-Konflikt in einem Notebook

Notebooks sind JSON — Merge-Konflikte darin sind hässlich. Verhindern:

- **Pro Sitzung nur einen aktiven Spawn** — wenn ihr zwischen gauss und euler wechselt, vorher pushen
- Vor Sitzungsende: pushen
- Nächste Sitzung: nach dem Spawn `git pull`, bevor ihr arbeitet

Wenn der Konflikt schon da ist: bittet den Lehrer um Hilfe — Notebooks per Hand zu mergen ist unangenehm.

### CSV-Annotation: Workflow lokal ↔ Jupyterhub

Empfohlen:

1. **Lokal annotieren** in Excel/LibreOffice (komfortabler als CSV-Edit im Browser)
2. **Hochladen** zu Jupyterhub: im File-Browser ⬆-Icon → Datei in `annotation/`
3. **Validieren** im Jupyterhub-Terminal: `python annotation/validate.py annotation/meine_gold.csv`
4. **Commit + push** im Jupyterhub-Terminal — der Repo-Stand lebt dort

Achtung: nicht in beiden Welten gleichzeitig editieren. Lokal ist *Edit-only*, Jupyterhub ist *Source of truth*.

### Versehentlich was Großes committed

```bash
git rm --cached predictions_grosse_datei.jsonl
git commit -m "remove accidentally tracked large file"
git push
```

Dann in `.gitignore` aufnehmen, falls noch nicht drin:

```bash
echo "predictions_*.jsonl" >> .gitignore
git add .gitignore
git commit -m "ignore predictions"
```

### "Ich hab alles kaputt gemacht"

```bash
git status               # erstmal lesen, nichts machen
git diff                 # was hat sich geändert?
```

Wenn ihr die letzten Änderungen wegwerfen wollt (Vorsicht — endgültig):

```bash
git checkout -- datei.ipynb     # einzelne Datei zurücksetzen
git reset --hard HEAD            # ALLES uncommittete weg
```

Wenn ihr unsicher seid: **fragt erst, bevor ihr `--hard` benutzt.** Das löscht eure Arbeit unwiederbringlich.

## Repo am Ende der LS — was zur Bewertung steht

Beim Fachgespräch öffnet der Lehrer euer Repo auf GitHub. Erwartete Inhalte:

```
notebooks/
  01_explore.ipynb              ✓ Phase 1 Bias-Notiz, Phase 2 κ + Edge Cases
  02_extract.ipynb              ✓ Pipeline + Iterationen
  03_eval.ipynb                 ✓ Per-Field-Accuracy + Iterations-Tabelle + Synthese
  04_frontier_compare.ipynb     ✓ κ Mensch ↔ Frontier
annotation/
  meine_gold.csv                ✓ 12 Anzeigen, validate.py-konform
  partner_gold.csv              ✓ Partner-CSV als Vergleichsbasis
  frontier_gold.csv             ✓ Frontier-Annotation
daten/
  eigener_korpus.jsonl          ✓ ≥30 Anzeigen aus Phase 1
memo_make_or_buy.md             ✓ 1-Seiter aus Phase 5
```

Plus Commit-History — die zeigt euren **Prozess**. Ein einziger Mega-Commit am letzten Tag riskiert Stufe 1 in Bereich 1 (siehe `BEWERTUNG/kriterien.md`).
