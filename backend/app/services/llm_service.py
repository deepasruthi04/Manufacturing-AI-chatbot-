import json
import requests
from app.core.config import settings

# In a real app, these would come from settings
GEMINI_API_KEY = "AIzaSyBq6-kSWBWZ62EYJd4dk1FRSxmdaJV9bgg"
MODEL = "gemini-2.0-flash" # Updated to a more standard model name if needed, keeping 1.5/2.0 logic
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

def _call_gemini(system_prompt: str, user_prompt: str, temp: float, top_p: float = 1.0) -> str:
    data = {
        "systemInstruction": {"parts": {"text": system_prompt}},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {"temperature": temp, "topP": top_p}
    }
    try:
        response = requests.post(GEMINI_URL, json=data)
        response_json = response.json()
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ LLM error: {response_json.get('error', response_json)}"
    except Exception as e:
        return f"⚠️ LLM error: {e}"

COMPANY_SYSTEM = """
You are an expert assistant for a manufacturing company.
Answer questions ONLY using the provided company documents context below.
If the answer is not in the context, say:
"This information is not available in the company documents."

Be extremely crisp, sharp, factual, and structured.
Your response MUST be formatted as exactly 3 concise bullet points.
Do NOT hallucinate or add information not present in the documents.
"""

MACHINE_SYSTEM = """
You are an Industry 4.0 manufacturing analyst specialized in OEE diagnostics.

You will receive:
1. OEE DATA – raw metrics fetched from MongoDB for the requested machine/line/plant.
2. INDUSTRY RULES – relevant rules and benchmarks from the company's Industry 4.0 ruleset document.

Your task: Analyse the OEE data and explain why OEE is low (or performing well) by cross-referencing the industry rules.

OUTPUT FORMAT (MANDATORY):

**1. PRIMARY ROOT CAUSE:**
- One word ONLY: Availability / Performance / Quality

**2. ROOT CAUSE ANALYSIS:**
- Exactly 3 bullet points
- Each bullet MUST cite at least one numeric value from the DATA
- Explain WHY the root cause occurred, referencing the INDUSTRY RULES where relevant


**3. IMPROVEMENT RECOMMENDATIONS:**
- Exactly 3 actionable bullet points
- Each must reference DATA values AND suggest a corrective action aligned with the INDUSTRY RULES

STRICT CONSTRAINTS:
- Total response: 15-20 lines MAX
- Do NOT include preambles, conclusions, or conversational text
- Do NOT hallucinate metrics not present in the DATA
- Do NOT use raw database variable names (like 'oee_percentage', 'downtime_minutes'). Translate them into natural, readable language (e.g., 'OEE', 'Downtime').
"""

GENERAL_SYSTEM = """
You are an expert Industry 4.0 and Manufacturing analyst.
Answer general knowledge questions about manufacturing KPIs, OEE, availability,
performance, quality, downtime, lean manufacturing, and related concepts.

Rules:
- Keep responses concise and structured (max 10 lines)
- Use bullet points where helpful
- Do NOT reference specific machines, dates, or database collections
"""

def answer_company_question(question: str, rag_context: str) -> str:
    prompt = f"""COMPANY DOCUMENTS CONTEXT:
{rag_context}

USER QUESTION:
{question}

Answer using ONLY the above context:"""
    return _call_gemini(COMPANY_SYSTEM, prompt, temp=0.1)

def answer_machine_question(question: str, mongo_data: list, rag_rules_context: str) -> str:
    if not mongo_data:
        return "⚠️ No data found in MongoDB for the specified machine / date."
    
    data_str = json.dumps(mongo_data, indent=2, default=str)
    prompt = f"""OEE DATA (from MongoDB):
{data_str}

INDUSTRY RULES (from RAG documents):
{rag_rules_context}

USER QUESTION:
{question}

Provide your analysis:"""
    return _call_gemini(MACHINE_SYSTEM, prompt, temp=0.0, top_p=0.1)

def answer_general_question(question: str) -> str:
    return _call_gemini(GENERAL_SYSTEM, question, temp=0.3)
