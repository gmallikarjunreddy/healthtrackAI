"""
HealthTrackAI — Gemini 3.1 Flash Lite AI Agent
Powers: report analysis, risk prediction, medicine suggestions, health chat
"""
import os, re, json
from dotenv import load_dotenv
load_dotenv()

from utils.medicine_database import get_medicine_suggestions, format_medicine_table

import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if GOOGLE_API_KEY and GOOGLE_API_KEY != "your_google_gemini_api_key_here":
    genai.configure(api_key=GOOGLE_API_KEY)

MODEL = "gemini-3.1-flash-lite-preview"

# ── System prompts ─────────────────────────────────────────────────────────────

ANALYSIS_SYSTEM = """You are HealthTrackAI, a world-class medical AI companion.
You analyze lab reports with the precision of a senior physician and explain results with the warmth of a caring family doctor.

PERSONALITY: Warm, empathetic, clear, encouraging. Never alarmist. Use simple English.

RESPONSE FORMAT — always use EXACTLY these section headers:

### 📊 KEY FINDINGS
For each biomarker found, use this exact format:
- **[Name]**: [Value] | Normal: [range] | Status: [🟢 Normal / 🟡 Borderline / 🔴 Abnormal / ⚠️ Critical]

### ⚠️ RISK ASSESSMENT
- **[Risk Name]** — [Low/Medium/High] risk — [1-sentence explanation]

### 💊 MEDICINES, STORES & PRICING
For each suggestion, provide:
- **[Medicine/Supplement Name]** (Generic name is best)
  - **Purpose**: [Brief reason]
  - **Dosage**: [Standard dosage or "As prescribed"]
  - **Approx. Price**: [Estimated price in Indian Rupees (₹). Example: ₹50 - ₹150]
  - **Where to Buy**: [Indian Stores: Apollo, MedPlus, Jan Aushadhi (Generic), NetMeds, 1mg]

### 🏥 SUGGESTED HOSPITALS & CARE
- **Specialist Needed**: [e.g. Cardiologist, Endocrinologist]
- **Facility Type**: [e.g. General Hospital, Specialized Clinic]
- **Search Recommendation**: "Best [Specialist] near me"
- **Top Hospital Chains**: [Suggest major Indian chains like Apollo, Fortis, Max, AIIMS, or local reputable hospitals]
(If report contains facility name/address, list it here as "Report Source")

### 🥗 DIET RECOMMENDATIONS
Specific foods to add and avoid, with reasons.

### 🏃 LIFESTYLE HABITS
5 specific, actionable daily habits tailored to these results.

### 💬 DOCTOR CONSULTATION ADVICE
What to discuss with the doctor at next visit.

### HEALTH_SCORE_JSON
At the very end output ONLY this line (valid JSON, no extra text):
SCORE:{"overall":75,"vitals":80,"nutrition":60,"risk":35,"label":"Fair Health","summary":"Brief 1-sentence summary"}

RULES:
- Never definitively diagnose. Use: "suggests", "may indicate", "consistent with"
- Always end analysis with: ⚕️ This analysis is informational only. Consult a licensed physician before any medical decision.
- Be extra gentle and hopeful with serious findings
"""

CHAT_SYSTEM = """You are HealthTrackAI, a humble AI health assistant. You are in a polite health consultation chat.

Be very short, simple, and polite. Use simple Indian English.
Use emojis sparingly 🇮🇳⚕️
For symptoms or test questions: give short answers with Indian context.
When recommending medicines: Use Indian Brand names, pricing in Rupees (₹) ONLY, and suggest stores like Apollo Pharmacy, MedPlus, or Jan Aushadhi.
When asked about hospitals: suggest specialists and major Indian hospitals.
Always recommend seeing a doctor for serious concerns.
Never diagnose definitively. Keep responses strictly under 150 words."""


class HealthAgent:

    def __init__(self):
        self._analysis_model = None
        self._chat_model = None

    def _get_analysis_model(self):
        if not self._analysis_model:
            self._analysis_model = genai.GenerativeModel(
                model_name=f"models/{MODEL}" if not MODEL.startswith("models/") else MODEL,
                system_instruction=ANALYSIS_SYSTEM,
            )
        return self._analysis_model

    def _get_chat_model(self):
        if not self._chat_model:
            self._chat_model = genai.GenerativeModel(
                model_name=f"models/{MODEL}" if not MODEL.startswith("models/") else MODEL,
                system_instruction=CHAT_SYSTEM,
            )
        return self._chat_model

    # ── Report Analysis ────────────────────────────────────────────────────────

    def analyze_report(self, text: str, filename: str, report_type: str) -> dict:
        prompt = f"""Analyze this {report_type} from file '{filename}'.

REPORT CONTENT:
{text[:5500]}

Give the complete structured analysis. Include the SCORE JSON at the end."""
        try:
            resp = self._get_analysis_model().generate_content(prompt)
            result = self._parse_response(resp.text)
            
            # 🩺 Rule-Based Pricing Engine
            meds = get_medicine_suggestions(result["analysis"])
            if meds:
                result["analysis"] += format_medicine_table(meds)
                
            return result
        except Exception as e:
            return {"analysis": f"❌ Analysis error: {e}\n\nCheck GOOGLE_API_KEY in .env",
                    "health_score": 0, "breakdown": {}, "error": str(e)}

    def _parse_response(self, raw: str) -> dict:
        score, breakdown = 70, {"vitals": 70, "nutrition": 65, "risk": 40, "label": "Fair Health", "summary": ""}
        m = re.search(r'SCORE:\s*(\{[^}]+\})', raw)
        if m:
            try:
                d = json.loads(m.group(1))
                score = d.get("overall", 70)
                breakdown = {k: d.get(k, v) for k, v in breakdown.items()}
                raw = raw[:m.start()].strip()
            except Exception:
                pass
        return {"analysis": raw.strip(), "health_score": score, "breakdown": breakdown, "error": None}

    # ── Chat ───────────────────────────────────────────────────────────────────

    def chat(self, message: str, history: list[dict], report_context: str = "") -> str:
        try:
            gemini_hist = []
            for m in history[-24:]:
                role = "user" if m["role"] == "user" else "model"
                gemini_hist.append({"role": role, "parts": [m["content"]]})

            if report_context and not gemini_hist:
                message = f"[Lab context: {report_context[:800]}]\n\nUser: {message}"
                c = self._get_chat_model().start_chat(history=[])
            else:
                c = self._get_chat_model().start_chat(history=gemini_hist[:-1] if gemini_hist else [])

            reply = c.send_message(message).text
            
            # 🩺 Check for medicine keywords in reply or question to append pricing
            meds = get_medicine_suggestions(reply + " " + message)
            if meds:
                reply += format_medicine_table(meds)
                
            return reply
        except Exception as e:
            return f"💙 Connection issue: {e}\n\nPlease verify your GOOGLE_API_KEY."

    # ── Health Summary ─────────────────────────────────────────────────────────

    def overall_summary(self, reports: list[dict]) -> str:
        if not reports:
            return "No reports yet — upload your first lab report to get started! 💙"
        context = "\n\n".join([
            f"[{r['report_type']}] Score: {r.get('health_score','?')}/100\n{r.get('analysis','')[:600]}"
            for r in reports[:5]
        ])
        prompt = f"""Based on these {len(reports)} lab reports, write a warm, clear overall health summary.
Include: current health status, top 3 concerns, top 3 wins, 3 priority action items, and an encouraging closing.
Keep it under 400 words. Be warm and motivating.

{context}"""
        try:
            return self._get_analysis_model().generate_content(prompt).text
        except Exception as e:
            return f"Could not generate summary: {e}"

    # ── Smart Questions ────────────────────────────────────────────────────────

    def suggest_questions(self, report_type: str) -> list[str]:
        qs = {
            "Blood Report (CBC)": ["What do my hemoglobin levels mean?", "Am I at risk of anemia?",
                                   "What foods boost my blood count?", "Is my WBC count normal?"],
            "Vitamin Panel": ["How much Vitamin D should I take?", "Can low B12 cause my fatigue?",
                              "Best foods for my deficiencies?", "Should I take supplements?"],
            "Thyroid Function": ["What does my TSH level mean?", "Do I have hypothyroidism?",
                                 "How does thyroid affect my weight?", "Best foods for thyroid?"],
            "Lipid Panel": ["Is my cholesterol dangerous?", "How to lower my LDL naturally?",
                            "Do I need statins?", "Best anti-cholesterol foods?"],
            "Diabetes Panel": ["Am I pre-diabetic?", "What does HbA1c mean?",
                               "Best diet for blood sugar control?", "How much exercise helps?"],
            "Liver Function": ["Is my liver healthy?", "What causes elevated liver enzymes?",
                               "Foods to avoid for liver health?", "Do I need treatment?"],
        }
        return qs.get(report_type, ["Explain my results simply", "What are my health risks?",
                                     "What supplements do I need?", "What lifestyle changes help?"])


import streamlit as st

_agent_instance = None

@st.cache_resource
def get_agent() -> HealthAgent:
    return HealthAgent()
