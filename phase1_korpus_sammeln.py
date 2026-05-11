"""
Phase 1b — Korpus gezielt um Vielfalt ergänzen
Hängt Ausbildung/Praktikum/Werkstudent-Anzeigen an bestehende JSONL an.
"""
import requests
import json
import base64
import time
import os
import re
import html

BASE_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4"
HEADERS = {
    "X-API-Key": "jobboerse-jobsuche",
    "User-Agent": (
        "Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; "
        "build:1077; iOS 15.1.0) Alamofire/5.4.4"
    ),
    "Accept": "application/json",
}
EXTERNE_PREFIXE = ("11949-", "12634-", "12288-", "14225-")

# Gezielte Nachsammlung — angebotsart 4 = Ausbildung, 34 = Praktikum/Trainee
NACH_QUERIES = [
    {"was": "Fachinformatiker Anwendungsentwicklung", "angebotsart": 4},
    {"was": "Fachinformatiker Daten",                 "angebotsart": 4},
    {"was": "Mathematisch-technischer Softwareentw",  "angebotsart": 4},
    {"was": "Praktikum Data Science",                 "angebotsart": 34},
    {"was": "Praktikum Datenanalyse",                 "angebotsart": 34},
    {"was": "Werkstudent Data",                       "angebotsart": 1},
    {"was": "Werkstudent Business Intelligence",      "angebotsart": 1},
    {"was": "Werkstudent Machine Learning",           "angebotsart": 1},
]

ZIEL_NACHSAMMLUNG = 20   # ~20 neue Anzeigen für Vielfalt
SEITEN_PRO_QUERY  = 3
PAGE_SIZE         = 25
PAUSE_SEKUNDEN    = 1.0
KORPUS_PFAD       = "daten/eigener_korpus.jsonl"


def ist_extern(refnr):
    return refnr.startswith(EXTERNE_PREFIXE)


def text_bereinigen(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def suche(query_params, page=1):
    params = {"size": PAGE_SIZE, "page": page, **query_params}
    r = requests.get(f"{BASE_URL}/jobs", headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    angebote = data.get("stellenangebote") or []
    print(f"  → Seite {page}: {len(angebote)} Treffer")
    return angebote


def detail_abrufen(refnr, retries=2):
    encoded = base64.b64encode(refnr.encode()).decode()
    url = f"{BASE_URL}/jobdetails/{encoded}"
    for versuch in range(retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(5)
                continue
            return None
        except requests.RequestException:
            if versuch < retries:
                time.sleep(2)
                continue
            return None
    return None


def anzeige_normalisieren(eintrag, detail):
    ort = eintrag.get("arbeitsort") or {}
    loks = detail.get("stellenlokationen") or []
    lok = loks[0] if loks else {}
    return {
        "refnr":  eintrag.get("refnr", ""),
        "titel":  detail.get("stellenangebotsTitel") or eintrag.get("titel", ""),
        "firma":  detail.get("firma") or eintrag.get("arbeitgeber", ""),
        "text":   text_bereinigen(detail.get("stellenangebotsBeschreibung", "")),
        "angebotsart":     detail.get("stellenangebotsart"),
        "veroeffentlicht": detail.get("datumErsteVeroeffentlichung"),
        "vollzeit":        detail.get("arbeitszeitVollzeit"),
        "vertragsdauer":   detail.get("vertragsdauer"),
        "ort_plz":         lok.get("plz") or ort.get("plz"),
        "ort_ort":         lok.get("ort") or ort.get("ort"),
        "ort_region":      lok.get("region") or ort.get("region"),
    }


def main():
    # Vorhandene refnrs einlesen → Duplikate vermeiden
    bereits = set()
    if os.path.exists(KORPUS_PFAD):
        with open(KORPUS_PFAD, encoding="utf-8") as f:
            for line in f:
                bereits.add(json.loads(line)["refnr"])
        print(f"📂 Bestehender Korpus: {len(bereits)} Anzeigen")
    else:
        print(f"⚠ Keine bestehende JSONL gefunden — wird neu angelegt")

    neu_count = 0
    stats = {"extern": 0, "kein_text": 0, "duplikat": 0, "detail_fehler": 0}

    print(f"\nZiel: +{ZIEL_NACHSAMMLUNG} neue Anzeigen für Vielfalt\n")

    # APPEND-Modus — bestehende Einträge bleiben erhalten
    with open(KORPUS_PFAD, "a", encoding="utf-8") as f_out:

        for query in NACH_QUERIES:
            if neu_count >= ZIEL_NACHSAMMLUNG:
                break

            art_label = {1: "Werkstudent/Arbeit", 4: "Ausbildung",
                         34: "Praktikum"}.get(query.get("angebotsart"), "?")
            print(f"\n🔍 \"{query['was']}\" ({art_label})")

            for page in range(1, SEITEN_PRO_QUERY + 1):
                if neu_count >= ZIEL_NACHSAMMLUNG:
                    break
                try:
                    treffer = suche(query, page)
                except Exception as e:
                    print(f"  ✗ {e}")
                    break
                if not treffer:
                    break

                for e in treffer:
                    if neu_count >= ZIEL_NACHSAMMLUNG:
                        break

                    refnr = e.get("refnr", "")
                    if not refnr or refnr in bereits:
                        stats["duplikat"] += 1
                        continue
                    if ist_extern(refnr):
                        stats["extern"] += 1
                        continue

                    time.sleep(PAUSE_SEKUNDEN)
                    detail = detail_abrufen(refnr)
                    if not detail:
                        stats["detail_fehler"] += 1
                        continue

                    text = text_bereinigen(
                        detail.get("stellenangebotsBeschreibung", "")
                    )
                    if len(text) < 100:
                        stats["kein_text"] += 1
                        continue

                    anzeige = anzeige_normalisieren(e, detail)
                    bereits.add(refnr)
                    neu_count += 1

                    f_out.write(json.dumps(anzeige, ensure_ascii=False) + "\n")
                    f_out.flush()

                    print(f"    ✓ [+{neu_count:>2}] "
                          f"{anzeige['titel'][:50]}  —  {anzeige['firma'][:25]}")

    print(f"\n{'─'*60}")
    print(f"✅ {neu_count} neue Anzeigen angehängt an {KORPUS_PFAD}")
    print(f"   Korpus gesamt: {len(bereits)} Anzeigen")
    print(f"   Übersprungen: {stats['extern']} extern, "
          f"{stats['kein_text']} kein Text, {stats['duplikat']} Duplikate, "
          f"{stats['detail_fehler']} Detail-Fehler")


if __name__ == "__main__":
    main()