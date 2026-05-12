import re
import requests
from typing import Dict, Any

# Using the same key/URL as in previous files for consistency
GEMINI_API_KEY = "AIzaSyBq6-kSWBWZ62EYJd4dk1FRSxmdaJV9bgg"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

_DEVICE_RE = re.compile(r"\b([A-Z]{2,6}_\d{3,})\b")
_DATE_RE    = re.compile(r"\b(\d{4}[-/]\d{2}[-/]\d{2})\b")
_LINE_RE    = re.compile(r"\bline\s*[:\-]?\s*(\d+)\b", re.IGNORECASE)
_PLANT_RE   = re.compile(r"\bplant\s*[:\-]?\s*(\d+)\b", re.IGNORECASE)

_MACHINE_KEYWORDS = {
    "oee", "availability", "performance", "quality", "downtime", "production",
    "machine", "device", "rejection", "idle", "utilization", "shift",
    "capacity", "output", "target", "actual", "energy", "line", "plant",
}

_COMPANY_KEYWORDS = {
    "company", "organization", "policy", "vision", "mission", "goal",
    "ruleset", "rule", "guideline", "standard", "iso", "industry 4.0",
    "about", "profile", "who are", "what does", "describe",
}

def extract_entities(question: str) -> Dict[str, Any]:
    q = question.strip()

    device_match = _DEVICE_RE.search(q)
    line_match   = _LINE_RE.search(q)
    plant_match  = _PLANT_RE.search(q)
    date_match   = _DATE_RE.search(q)

    device_id = device_match.group(1) if device_match else None
    line_id   = line_match.group(1)   if line_match   else None
    plant_id  = plant_match.group(1)  if plant_match  else None
    date      = date_match.group(1).replace("/", "-") if date_match else None

    if device_id:
        level = "machine"
    elif line_id:
        level = "line"
    elif plant_id:
        level = "plant"
    else:
        level = None

    ql = q.lower()
    if "month" in ql or "monthly" in ql:
        period = "month"
    elif "week" in ql or "weekly" in ql:
        period = "week"
    elif "year" in ql or "annual" in ql:
        period = "year"
    else:
        period = "day"

    return {
        "device_id": device_id,
        "line_id": line_id,
        "plant_id": plant_id,
        "date": date,
        "level": level,
        "period": period,
    }

def classify_intent(question: str) -> str:
    q_lower = question.lower()
    tokens  = set(re.findall(r"\w+", q_lower))

    if _DEVICE_RE.search(question) or _LINE_RE.search(question) or _PLANT_RE.search(question):
        return "machine"

    machine_hits = tokens & _MACHINE_KEYWORDS
    company_hits = tokens & _COMPANY_KEYWORDS

    if company_hits and not machine_hits:
        return "company"

    if machine_hits and not company_hits:
        return "machine"

    try:
        data = {
            "systemInstruction": {
                "parts": {"text": "You are a routing classifier. Classify the user question into exactly one of these categories: 'company', 'machine', 'general'. Respond with ONLY one word."}
            },
            "contents": [{"parts": [{"text": question}]}],
            "generationConfig": {"temperature": 0.0}
        }
        response = requests.post(GEMINI_URL, json=data)
        response_json = response.json()
        if "candidates" in response_json:
            intent_raw = response_json["candidates"][0]["content"]["parts"][0]["text"]
            intent = intent_raw.strip().lower().split()[0]
            if intent in {"company", "machine", "general"}:
                return intent
    except Exception:
        pass

    return "general"
