# Jupyterhub + GPU — Cheatsheet

**Wann ihr das braucht:** Phase 3 + 4 + 6 — alle Pipeline-Runs.

## Server-Übersicht

| Server | GPU | VRAM | Tauglich für |
|---|---|---|---|
| **gauss** | 4× V100 SXM2 | 32 GB pro GPU | Qwen2.5-7B fp32 (knapp!) |
| **euler** | 4× V100 SXM2 | 16 GB pro GPU | Qwen2.5-3B fp32 (komfortabel) |

7B läuft **nur auf gauss**. 3B läuft auf beiden, primär aber auf **euler** — damit gauss frei für 7B bleibt.

**Home-Verzeichnis ist zwischen gauss und euler synchronisiert.** Eure Notebooks und CSV-Dateien wandern automatisch mit.

## Jupyterhub-Spawn

Im Browser einloggen, Spawn-Dialog wählen:
- **Server:** gauss (für 7B in Phase 3-5) oder euler (für 3B in Phase 6)
- **GPU:** der Spawn weist euch eine zu

Nach dem Spawn landet ihr im Jupyter-File-Browser. Euer Repo (geklont — siehe unten) erscheint hier als Verzeichnis.

## Repo klonen

Jupyterhub-Terminal öffnen (oben rechts `+` → Terminal):

```bash
cd ~                                                       # /home/jovyan
git clone https://github.com/<euer-username>/ls-information-extraction.git
cd ls-information-extraction
```

GitHub fragt beim Clone (oder beim ersten `git push`) nach Username + Personal Access Token — Setup siehe `git-grundlagen.md`. **SSH geht im Schulnetz nicht** (Port gesperrt), deshalb HTTPS + Token.

Da Home synchronisiert ist: **einmal klonen reicht** für gauss + euler.

## GPU im Notebook wählen

Erst prüfen, was zugewiesen ist:

```python
import os
print(os.environ.get("CUDA_VISIBLE_DEVICES", "(nicht gesetzt — alle sichtbar)"))

import torch
print(f"verfügbare GPUs: {torch.cuda.device_count()}")
print(f"aktive GPU: {torch.cuda.current_device()} = {torch.cuda.get_device_name(0)}")
```

Falls ihr explizit eine GPU wählen müsst (z. B. Spawn hat alle 4 zugeteilt):

```python
# AM ANFANG des Notebooks, VOR dem Modell-Load:
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"   # 0, 1, 2 oder 3
```

## Klassen-Koordination

Mit 6 Schüler:innen auf 4 GPUs:
- Sitzplatz-Mapping per Whiteboard: "Sitz 1 → GPU 0", "Sitz 2 → GPU 1", …
- Plätze 5 + 6 warten ~6 min, bis ein Run durch ist
- Auf euler ist's weniger eng — 3B parallel auf allen 4 GPUs läuft

## Datei-Upload/Download (für CSV-Annotation)

Vom Schul-Rechner zu Jupyterhub:
- Im File-Browser ⬆-Icon → Datei wählen, ins richtige Verzeichnis (z. B. `annotation/`)
- Oder per Drag & Drop

Zurück:
- Rechtsklick auf Datei → Download

Typischer Annotations-Workflow:

1. **Lokal annotieren** in LibreOffice/Excel — komfortabler als CSV-Edit im Browser
2. **Hochladen** → `annotation/meine_gold.csv`
3. **Validieren** im Terminal: `python annotation/validate.py annotation/meine_gold.csv`
4. **Committen + pushen** im Terminal — der Repo-Stand lebt dort

## Modelle laden

Modelle sind **bereits gecached** auf gauss + euler:

```
/home/jovyan/.cache/huggingface/
```

Kein Download nötig. Erster `from_pretrained()`-Aufruf liest aus dem Cache (~9 s für 7B, ~6 s für 3B). Wenn ihr einen falschen Modell-Namen verwendet, triggert das einen 28-GB-Download → Bandbreiten-Bremse für die Klasse. Achtet auf die exakten Namen aus `transformers-konzepte.md`.

## Memory — kritisch beim 7B

Qwen2.5-7B fp32 belegt **31,6 GB von 32 GB**. Auf der Kante:
- **Truncation initial ~2000 Zeichen** — nicht hochsetzen ohne OOM-Risiko
- **`max_new_tokens=200`** reicht für unser Schema
- **Batch-Size = 1** zwingend (sequenzielle Inferenz)

Wenn OOM (`torch.cuda.OutOfMemoryError`):
1. Kernel-Restart (Kernel → Restart) — Speicher freigegeben
2. `nvidia-smi` checken — läuft jemand anders auf eurer GPU?
3. Truncation reduzieren

## GPU-Auslastung prüfen

Im Terminal:

```bash
nvidia-smi
```

Pro GPU: belegter Speicher, laufende Prozesse, Auslastung. Wenn eure Karte voll ist → Sitz-Mapping verletzt → kurz absprechen.

## Performance-Erwartungen

| Aktion | Dauer |
|---|---|
| Cold Start 7B (gauss) | ~10 s |
| Cold Start 3B (euler) | ~6 s |
| Inferenz pro Anzeige (7B fp32) | 3,1 – 4,7 s |
| Inferenz pro Anzeige (3B fp32) | 3,7 – 4,2 s |
| 30-Anzeigen-Run (7B) | ~2 min |
| 30-Anzeigen-Run (3B) | ~2 min |

Wenn euer Run signifikant langsamer ist: GPU geteilt? `nvidia-smi`.

## Häufige Fehler

| Symptom | Ursache | Lösung |
|---|---|---|
| Jupyterhub-Login dreht sich endlos | VPN aus | `bash ~/vpn/start_vpn.sh` |
| `CUDA out of memory` | GPU geteilt oder Text zu lang | `nvidia-smi` / Truncation senken |
| Modell-Output ist Token-Salat | fp16/bf16 statt fp32 | `torch_dtype=torch.float32` |
| Run hängt bei "Loading checkpoint shards" | Cache-Miss, Download läuft | falscher Modell-Name? Lehrer fragen |
| Server-Switch — Notebook hängt | Spawn auf falschem Server | beim Spawn richtig wählen, nicht mid-session switchen |

## Disclaimer

Diese Setup-Konfiguration ist auf der Kante balanciert (7B fp32 in 32 GB) und für unsere Pipeline mit getesteten Parametern verifiziert. **Experimentiert nicht mit Quantisierung oder Datentypen außerhalb der Vorgaben** — fp16/bf16 ist auf V100 + Qwen2.5 nicht stabil. Wenn ihr eine Variante probieren wollt, fragt vorher.
