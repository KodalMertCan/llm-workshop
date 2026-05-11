# Cheatsheets

Kurze Referenz-Blätter zu Werkzeugen und Formaten, die ihr in den Phasen trefft. Ein Blatt ≈ eine Seite, schlagt punktuell nach.

- `jsonl.md` — Was JSONL ist, wie es sich von JSON unterscheidet, wie ihr in Python damit lest/schreibt (relevant ab Phase 1)
- `git-grundlagen.md` — Setup, daily workflow, Commit-Messages mit Zahlen-Belegen, Notebook-Konflikte vermeiden, häufige Probleme (durchgängig)
- `transformers-konzepte.md` — Modell-Namen, lauffähiges Mini-Beispiel mit Chat-Template, Hardware-Fallen (kein `device_map`, kein fp16), robustes JSON-Parsing, Generation-Parameter (vor Phase 3 lesen)
- `gpu-zugang.md` — Jupyterhub-Spawn (gauss/euler), VPN, GPU-Wahl per `os.environ`, Datei-Upload/Download, Memory-Constraints, Performance-Erwartungen (Phase 3 + 4 + 6)
- `kappa.md` — Cohen's κ: Anschauung, Formel, Rechenbeispiel von Hand, Interpretation (Landis & Koch), Anwendung mit `validate.py`, häufige Fallen (Phase 2 + 5)
- `frontier-llm-workflow.md` — Eingabe-Block-Format für Web-Chat (Claude/ChatGPT), Workflow Schritt für Schritt, Schema-Verletzungs-Handling, DSGVO (Phase 5)
