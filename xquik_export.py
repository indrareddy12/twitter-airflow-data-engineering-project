import csv
import json
from pathlib import Path


TEXT_FIELDS = ("text", "tweet", "full_text", "content", "body")


def _records_from_json(raw_text):
    payload = json.loads(raw_text)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "tweets", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("JSON export must contain a list of tweet objects.")


def _records_from_csv(raw_text):
    return list(csv.DictReader(raw_text.splitlines()))


def _record_text(record):
    for field in TEXT_FIELDS:
        value = record.get(field)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def load_xquik_rows(path):
    export_path = Path(path)
    raw_text = export_path.read_text(encoding="utf-8")
    suffix = export_path.suffix.lower()

    if suffix == ".json":
        records = _records_from_json(raw_text)
    elif suffix == ".jsonl":
        records = [json.loads(line) for line in raw_text.splitlines() if line.strip()]
    elif suffix == ".csv":
        records = _records_from_csv(raw_text)
    else:
        raise ValueError("Xquik export must be JSON, JSONL, or CSV.")

    rows = []
    for record in records:
        if not isinstance(record, dict):
            continue
        text = _record_text(record)
        if not text:
            continue
        rows.append(
            {
                "user": str(record.get("username") or record.get("user") or ""),
                "text": text,
                "favorite_count": record.get("like_count", record.get("favorite_count", 0)),
                "retweet_count": record.get("retweet_count", 0),
                "created_at": str(record.get("created_at", "")),
            }
        )

    if not rows:
        raise ValueError("Xquik export did not contain tweet text.")
    return rows
