from __future__ import annotations

from pathlib import Path
import csv
import sys

import requests

REQUIRED_FIELDS = {"id", "name", "email", "active"}


def fetch_json(url: str, timeout: int = 10):
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError("Expected a JSON array of records")
    return payload


def normalize_record(record: dict):
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")
    return {
        "id": str(record["id"]).strip(),
        "name": " ".join(str(record["name"]).split()),
        "email": str(record["email"]).strip().lower(),
        "active": bool(record["active"]),
    }


def transform(payload):
    rows = []
    for record in payload:
        normalized = normalize_record(record)
        if normalized["active"]:
            rows.append(normalized)
    return rows


def export_csv(rows, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "active"])
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def run(url: str, output_path: Path):
    payload = fetch_json(url)
    rows = transform(payload)
    return export_csv(rows, output_path), rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python api_automation.py <url> <output.csv>")
    path, rows = run(sys.argv[1], Path(sys.argv[2]))
    print(f"Exported {len(rows)} active records to {path}")
