#!/usr/bin/env python3
"""
Validiert eine Annotations-CSV oder Predictions-JSONL gegen das LS-Schema (siehe SCHEMA.md).

Drei Modi:

    python validate.py meine_gold.csv
        Schema-Check der Annotations-CSV.

    python validate.py meine_gold.csv --kappa-against partner_gold.csv
        Wie oben, plus Cohen's kappa zwischen zwei Annotator:innen.

    python validate.py --validate-jsonl predictions.jsonl
        Schema-Check einer Predictions-JSONL (Phase 6 — Modell-Output prüfen).
        Erwartet pro Zeile ein JSON-Objekt mit den Schema-Feldern.

Schema ist fix für die LS. Wer `ALLOWED` unten ändert, ändert das Schema.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ALLOWED = {
    "homeoffice": {"ja", "teilweise", "nein", "remote", "nicht_genannt"},
    "vertragsart": {"ausbildung", "festanstellung", "praktikum", "werkstudent", "sonstiges"},
    "erfahrungslevel": {"junior", "mid", "senior", "egal", "nicht_genannt"},
    "gehalt_zeitraum": {"monat", "jahr"},
}

CATEGORICAL_FIELDS = ["homeoffice", "vertragsart", "erfahrungslevel"]


# ---------- CSV-Validierung (Phase 2 + 5) ----------

def validate_csv_row(row: dict, line_no: int) -> list[str]:
    errors = []

    for field in CATEGORICAL_FIELDS:
        val = (row.get(field) or "").strip()
        if val not in ALLOWED[field]:
            errors.append(f"Zeile {line_no}: {field}={val!r} nicht in {sorted(ALLOWED[field])}")

    gehalt = (row.get("gehalt_min_eur") or "").strip()
    zeitraum = (row.get("gehalt_zeitraum") or "").strip()

    if gehalt:
        if not gehalt.isdigit():
            errors.append(f"Zeile {line_no}: gehalt_min_eur={gehalt!r} ist keine ganze Zahl")
        elif not zeitraum:
            errors.append(f"Zeile {line_no}: gehalt_min_eur gesetzt, aber gehalt_zeitraum leer")
    if zeitraum and zeitraum not in ALLOWED["gehalt_zeitraum"]:
        errors.append(
            f"Zeile {line_no}: gehalt_zeitraum={zeitraum!r} "
            f"nicht in {sorted(ALLOWED['gehalt_zeitraum'])}"
        )

    skills = (row.get("skills_top3") or "").strip()
    if skills:
        parts = [s.strip() for s in skills.split("|") if s.strip()]
        if len(parts) > 3:
            errors.append(f"Zeile {line_no}: skills_top3 hat {len(parts)} Einträge (max 3)")

    return errors


def load_annotations(path: Path) -> dict[str, dict]:
    """Liest CSV und indiziert nach id."""
    out = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = (row.get("id") or "").strip()
            if not rid:
                continue
            out[rid] = row
    return out


# ---------- Cohen's kappa (Phase 2 + 5) ----------

def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    """Cohen's kappa für zwei parallele Label-Listen (gleiche Länge)."""
    assert len(labels_a) == len(labels_b)
    n = len(labels_a)
    if n == 0:
        return float("nan")

    agreed = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agreed / n

    cat_a = Counter(labels_a)
    cat_b = Counter(labels_b)
    all_cats = set(cat_a) | set(cat_b)
    p_e = sum((cat_a[c] / n) * (cat_b[c] / n) for c in all_cats)

    if p_e == 1.0:
        # Cohen's kappa ist bei p_e == 1.0 mathematisch undefiniert (Division durch 0).
        # Beide Annotator:innen wählen durchgängig dieselbe Klasse — der Zufallsanteil
        # ist nicht identifizierbar, auch wenn p_o == 1.0 ist.
        return float("nan")
    return (p_o - p_e) / (1 - p_e)


def kappa_report(file_a: Path, file_b: Path) -> None:
    a = load_annotations(file_a)
    b = load_annotations(file_b)
    common_ids = sorted(set(a) & set(b), key=lambda x: int(x) if x.isdigit() else x)

    print(f"\nCohen's kappa: {file_a.name} vs. {file_b.name}")
    print(f"Gemeinsame IDs: {len(common_ids)}\n")

    print(f"{'Feld':<20} {'kappa':>8} {'Übereinst.':>12}")
    print("-" * 42)
    for field in CATEGORICAL_FIELDS:
        labels_a = [(a[i].get(field) or "").strip() for i in common_ids]
        labels_b = [(b[i].get(field) or "").strip() for i in common_ids]
        k = cohen_kappa(labels_a, labels_b)
        agree = sum(1 for x, y in zip(labels_a, labels_b) if x == y)
        pct = agree / len(common_ids) if common_ids else 0
        print(f"{field:<20} {k:>8.3f} {pct:>11.0%}")

    print("\nInterpretation (Landis & Koch 1977):")
    print("  < 0.00      schlechter als Zufall")
    print("  0.00–0.20   schlecht")
    print("  0.21–0.40   mäßig")
    print("  0.41–0.60   moderat")
    print("  0.61–0.80   substanziell")
    print("  0.81–1.00   fast perfekt")


# ---------- JSONL-Validierung (Phase 6) ----------

def validate_jsonl_record(obj: dict) -> list[str]:
    """Schema-Check für ein JSONL-Objekt (Modell-Output, native JSON-Typen)."""
    errors = []

    for field in CATEGORICAL_FIELDS:
        val = obj.get(field)
        if val is None or val == "":
            errors.append(f"{field}: leer")
            continue
        if not isinstance(val, str) or val not in ALLOWED[field]:
            errors.append(f"{field}: {val!r} nicht in Schema")

    gehalt = obj.get("gehalt_min_eur")
    zeitraum = obj.get("gehalt_zeitraum")

    if gehalt is not None:
        if not isinstance(gehalt, int) or isinstance(gehalt, bool):
            errors.append(f"gehalt_min_eur: {gehalt!r} ist kein int")
        elif zeitraum is None or zeitraum == "":
            errors.append("gehalt_zeitraum: leer trotz gehalt_min_eur")
    if zeitraum is not None and zeitraum != "" and zeitraum not in ALLOWED["gehalt_zeitraum"]:
        errors.append(f"gehalt_zeitraum: {zeitraum!r} nicht in Schema")

    skills = obj.get("skills_top3")
    if skills is not None:
        if not isinstance(skills, list):
            errors.append(f"skills_top3: kein Array, sondern {type(skills).__name__}")
        elif len(skills) > 3:
            errors.append(f"skills_top3: {len(skills)} Einträge (max 3)")

    return errors


def validate_jsonl_file(path: Path) -> int:
    parse_fails = 0
    total_records = 0
    field_violations = Counter()

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_records += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                parse_fails += 1
                continue
            for err in validate_jsonl_record(obj):
                field_violations[err] += 1

    print(f"\nJSONL Schema-Check: {path.name}")
    print(f"Geprüfte Zeilen: {total_records}")
    print(f"JSON-Parse-Fails: {parse_fails}")
    if field_violations:
        total = sum(field_violations.values())
        print(f"\n{total} Feld-Verletzungen (sortiert):")
        for desc, count in field_violations.most_common():
            print(f"  {count:>4}×  {desc}")
    else:
        print("Keine Feld-Verletzungen.")

    return 1 if (parse_fails or field_violations) else 0


# ---------- CLI ----------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validiert Annotations-CSV oder Predictions-JSONL gegen das LS-Schema."
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        nargs="?",
        help="Pfad zur Annotations-CSV (optional, wenn --validate-jsonl gesetzt)",
    )
    parser.add_argument(
        "--kappa-against",
        type=Path,
        default=None,
        help="Zweite CSV für Cohen's kappa (paarweiser Annotator-Vergleich)",
    )
    parser.add_argument(
        "--validate-jsonl",
        type=Path,
        default=None,
        help="Predictions-JSONL gegen Schema prüfen (Phase 6)",
    )
    args = parser.parse_args()

    if args.validate_jsonl:
        if not args.validate_jsonl.exists():
            print(f"FEHLER: {args.validate_jsonl} nicht gefunden", file=sys.stderr)
            return 2
        return validate_jsonl_file(args.validate_jsonl)

    if not args.csv_file:
        parser.error("entweder eine CSV-Datei oder --validate-jsonl erforderlich")

    if not args.csv_file.exists():
        print(f"FEHLER: {args.csv_file} nicht gefunden", file=sys.stderr)
        return 2

    all_errors = []
    with args.csv_file.open() as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            if not (row.get("id") or "").strip():
                continue
            all_errors.extend(validate_csv_row(row, line_no))

    if all_errors:
        print(f"\n{len(all_errors)} Schema-Verletzungen in {args.csv_file.name}:\n")
        for err in all_errors:
            print(f"  - {err}")
    else:
        print(f"OK: {args.csv_file.name} ist schema-konform.")

    if args.kappa_against:
        if not args.kappa_against.exists():
            print(f"FEHLER: {args.kappa_against} nicht gefunden", file=sys.stderr)
            return 2
        kappa_report(args.csv_file, args.kappa_against)

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
