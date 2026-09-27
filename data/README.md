# Public work-order data

The file [`public/nyc-parks-work-orders.json`](public/nyc-parks-work-orders.json) is a small, unchanged-field snapshot of **three actual NYC Parks AMPS work orders**. NYC Open Data publishes the [dataset](https://data.cityofnewyork.us/d/8sdw-8vja); the [Data.gov catalog](https://catalog.data.gov/dataset/asset-management-parks-system-amps-work-orders) identifies `EVT_CODE` as the work-order key and describes the work description and completion date fields.

| Official ID | Source description (`EVT_DESC`) | Published status |
|---|---|---|
| `2791739` | `install air conditioners` | `Completed` |
| `2792582` | `Inspect in/outdoor fridge  walk-in-boxes,heating,cooling and  complete logs` | `Completed` |
| `2792861` | `work on plant repairs with oiler HVAC units belts and filters` | `Completed` |

The JSON includes the exact API query, retrieval time, selected fields, and SHA-256 of canonicalized selected rows. Run `python3 data/refresh_public.py` to fetch the same IDs again. The source can change after this snapshot; the code deliberately keeps the committed snapshot offline so evaluation is reproducible.

These records are genuine **public operational metadata**, from New York City, not proof that an Indonesian SME uses the product. `EVT_DESC` is a work-order description, not a technician's final report. `Completed` and `EVT_COMPLETED` are database fields, not customer acceptance, physical inspection proof, or billing authorization. The selected public records do not provide the contract, photos, inspection logs, signed acceptance, or invoice. The Langflow public-record route therefore returns `INSUFFICIENT_EVIDENCE` and refuses to generate a billing pack. Its missing-item checks are prototype questions, **not asserted contract requirements for NYC Parks**.

The separate `WO-1028` AC walkthrough in `app/` and `demo/` remains fully synthetic and clearly labeled. No public record was joined to synthetic photos, readings, signatures, or a fabricated customer outcome.
