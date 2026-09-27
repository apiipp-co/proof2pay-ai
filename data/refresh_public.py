"""Capture three published NYC Parks work orders without altering source fields.

Run explicitly when a fresh public snapshot is wanted. The committed snapshot is
used offline by the Langflow flows; running this script never invents evidence.
"""

import hashlib
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DATASET = "8sdw-8vja"
FIELDS = ("evt_code", "evt_desc", "evt_type", "evt_date", "evt_completed", "evt_udfchar13", "evt_udfchar06")
IDS = (2791739, 2792582, 2792861)
QUERY = "https://data.cityofnewyork.us/resource/" + DATASET + ".json?" + urllib.parse.urlencode({
    "$select": ",".join(FIELDS),
    "$where": "evt_code in(" + ",".join(map(str, IDS)) + ")",
    "$order": "evt_code",
})
TARGET = Path(__file__).resolve().parent / "public" / "nyc-parks-work-orders.json"


def main():
    request = urllib.request.Request(QUERY, headers={"User-Agent": "Proof2Pay-public-data-reproducibility/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        rows = json.load(response)
    if [int(row["evt_code"]) for row in rows] != list(IDS):
        raise RuntimeError("Published record IDs differ from the expected three")
    if any(set(row) != set(FIELDS) for row in rows):
        raise RuntimeError("Published fields differ from the documented snapshot")
    canonical = json.dumps(rows, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    document = {
        "dataset": "NYC Parks Asset Management Parks System (AMPS) - Work Orders",
        "publisher": "New York City Department of Parks and Recreation via NYC Open Data",
        "dataset_url": "https://data.cityofnewyork.us/d/" + DATASET,
        "query_url": QUERY,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "selected_rows_sha256": hashlib.sha256(canonical).hexdigest(),
        "records": rows,
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    print(f"Saved {len(rows)} published records to {TARGET}")
    print("SHA-256:", document["selected_rows_sha256"])


if __name__ == "__main__":
    main()
