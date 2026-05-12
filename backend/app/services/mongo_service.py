from app.db.mongodb import mongodb_client
from app.core.config import settings
from typing import List, Dict, Any

def _coerce_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return val

def _resolve_db_and_collection(
    org_key: str,
    level: str,      # machine | line | plant
    period: str,     # day | month | week | year
    year: str,
    month: str,
):
    org_key = org_key.upper()
    level_cap = level.capitalize()
    mm = month.zfill(2)

    db_name = f"{org_key}_Analytics"

    col_map = {
        "day":   f"{year}_{mm}_{level_cap}_day",
        "month": f"{year}_{mm}_{level_cap}_month",
        "week":  f"{year}_{mm}_{level_cap}_weekly",
        "year":  f"{year}_{level_cap}_year",
    }
    collection_name = col_map.get(period, f"{year}_{mm}_{level_cap}_day")
    return db_name, collection_name

def fetch_machine_data(
    device_id: str,
    date: str,
    org_key: str = None,
    period: str = "day",
) -> List[Dict[str, Any]]:
    org_key = (org_key or settings.ORG_KEY or "ADM").upper()
    parts = date.replace("/", "-").split("-")
    year  = parts[0] if len(parts) >= 1 else "2026"
    month = parts[1] if len(parts) >= 2 else "01"

    db_name, col_name = _resolve_db_and_collection(org_key, "machine", period, year, month)
    db = mongodb_client.get_database(db_name)
    collection = db[col_name]

    filter_q: dict = {"deviceID": device_id}
    if period == "day":
        filter_q["anchorDate"] = date.replace("/", "-")
    elif period == "month":
        filter_q["month"] = month.zfill(2)

    docs = list(collection.find(filter_q, {}).limit(5))
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs

def fetch_line_data(
    line_id: Any,
    date: str,
    org_key: str = None,
    period: str = "day",
) -> List[Dict[str, Any]]:
    org_key = (org_key or settings.ORG_KEY or "ADM").upper()
    parts = date.replace("/", "-").split("-")
    year  = parts[0] if len(parts) >= 1 else "2026"
    month = parts[1] if len(parts) >= 2 else "01"

    db_name, col_name = _resolve_db_and_collection(org_key, "line", period, year, month)
    db = mongodb_client.get_database(db_name)
    collection = db[col_name]

    filter_q: dict = {"lineID": _coerce_int(line_id)}
    if period == "day":
        filter_q["anchorDate"] = date.replace("/", "-")
    elif period == "month":
        filter_q["month"] = month.zfill(2)

    docs = list(collection.find(filter_q, {}).limit(5))
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs

def fetch_plant_data(
    plant_id: Any,
    date: str,
    org_key: str = None,
    period: str = "day",
) -> List[Dict[str, Any]]:
    org_key = (org_key or settings.ORG_KEY or "ADM").upper()
    parts = date.replace("/", "-").split("-")
    year  = parts[0] if len(parts) >= 1 else "2026"
    month = parts[1] if len(parts) >= 2 else "01"

    db_name, col_name = _resolve_db_and_collection(org_key, "plant", period, year, month)
    db = mongodb_client.get_database(db_name)
    collection = db[col_name]

    filter_q: dict = {"plantID": _coerce_int(plant_id)}
    if period == "day":
        filter_q["anchorDate"] = date.replace("/", "-")
    elif period == "month":
        filter_q["month"] = month.zfill(2)

    docs = list(collection.find(filter_q, {}).limit(5))
    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])
    return docs
