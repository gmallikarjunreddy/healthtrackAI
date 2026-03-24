
"""
Medicine Database for HealthTrackAI
Rule-based pricing and store availability for common health issues.
Promotes Generic stores (Jan Aushadhi), MedPlus, and Apollo Pharmacy.
"""

MEDICINE_DB = {
    "fever": {
        "issue": "Fever / High Temperature",
        "medicine": "Paracetamol 650mg",
        "brands": ["Dolo 650", "Calpol 650", "P-650"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹15 (Strip of 15)",
            "MedPlus": "₹30 (Strip of 15)",
            "Apollo": "₹32 (Strip of 15)"
        }
    },
    "pain": {
        "issue": "Body Pain / Headache",
        "medicine": "Aceclofenac + Paracetamol",
        "brands": ["Zerodol-P", "Aceclo Plus"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹20 (Strip of 10)",
            "MedPlus": "₹55 (Strip of 10)",
            "Apollo": "₹60 (Strip of 10)"
        }
    },
    "acidity": {
        "issue": "Acidity / Gastritis",
        "medicine": "Pantoprazole 40mg",
        "brands": ["Pan 40", "Pantocid 40"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹22 (Strip of 10)",
            "MedPlus": "₹110 (Strip of 15)",
            "Apollo": "₹120 (Strip of 15)"
        }
    },
    "cold": {
        "issue": "Common Cold / Runny Nose",
        "medicine": "Levocetirizine 5mg",
        "brands": ["Levocet", "Teczine 5"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹15 (Strip of 10)",
            "MedPlus": "₹45 (Strip of 10)",
            "Apollo": "₹50 (Strip of 10)"
        }
    },
    "cough_dry": {
        "issue": "Dry Cough",
        "medicine": "Dextromethorphan Syrup",
        "brands": ["Alex Syrup", "Ascoril D"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹60 (100ml)",
            "MedPlus": "₹110 (100ml)",
            "Apollo": "₹125 (100ml)"
        }
    },
    "cough_wet": {
        "issue": "Wet Cough / Phlegm",
        "medicine": "Ambroxol + Guaiphenesin Syrup",
        "brands": ["Asthalin Expectorant", "Ascoril LS"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹55 (100ml)",
            "MedPlus": "₹105 (100ml)",
            "Apollo": "₹118 (100ml)"
        }
    },
    "antibiotic": {
        "issue": "Bacterial Infection (Consult Doctor)",
        "medicine": "Amoxicillin + Clavulanic Acid 625",
        "brands": ["Augmentin 625", "Moxikind-CV 625"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹120 (Strip of 6)",
            "MedPlus": "₹200 (Strip of 10)",
            "Apollo": "₹220 (Strip of 10)"
        }
    },
    "vitamin_d": {
        "issue": "Vitamin D Deficiency (Low Vitamin D)",
        "medicine": "Cholecalciferol 60K IU (Weekly)",
        "brands": ["Uprise-D3 60K", "Calcirol"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹25 (Pack of 4)",
            "MedPlus": "₹130 (Pack of 4)",
            "Apollo": "₹150 (Pack of 4)"
        }
    },
    "vitamin_b12": {
        "issue": "Vitamin B12 Deficiency",
        "medicine": "Methylcobalamin 1500mcg",
        "brands": ["Nurokind-OD", "Methycobal"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹35 (Strip of 10)",
            "MedPlus": "₹140 (Strip of 10)",
            "Apollo": "₹160 (Strip of 10)"
        }
    },
    "calcium": {
        "issue": "Calcium Deficiency / Bone Health",
        "medicine": "Calcium + Vitamin D3",
        "brands": ["Shelcal 500", "Cipcal 500"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹45 (Strip of 15)",
            "MedPlus": "₹115 (Strip of 15)",
            "Apollo": "₹130 (Strip of 15)"
        }
    },
    "iron": {
        "issue": "Iron Deficiency Anemia (Low Hemoglobin)",
        "medicine": "Ferrous Ascorbate + Folic Acid",
        "brands": ["Orofer-XT", "Livogen"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹50 (Strip of 10)",
            "MedPlus": "₹160 (Strip of 10)",
            "Apollo": "₹180 (Strip of 10)"
        }
    },
    "cholesterol": {
        "issue": "High Cholesterol / Lipids",
        "medicine": "Atorvastatin 10mg",
        "brands": ["Atorva 10", "Lipvas 10"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹20 (Strip of 10)",
            "MedPlus": "₹65 (Strip of 15)",
            "Apollo": "₹75 (Strip of 15)"
        }
    },
    "diabetes": {
        "issue": "Diabetes / High Blood Sugar (Type 2)",
        "medicine": "Metformin 500mg (SR)",
        "brands": ["Glycomet 500 SR", "Gluconorm"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹18 (Strip of 10)",
            "MedPlus": "₹40 (Strip of 15)",
            "Apollo": "₹45 (Strip of 15)"
        }
    },
    "bp": {
        "issue": "High Blood Pressure / Hypertension",
        "medicine": "Amlodipine 5mg",
        "brands": ["Amlong 5", "Stamlo 5"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹10 (Strip of 10)",
            "MedPlus": "₹35 (Strip of 15)",
            "Apollo": "₹40 (Strip of 15)"
        }
    },
    "thyroid": {
        "issue": "Hypothyroidism (High TSH)",
        "medicine": "Thyroxine Sodium 50mcg",
        "brands": ["Thyronorm 50", "Eltroxin 50"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹50 (Bottle of 100)",
            "MedPlus": "₹140 (Bottle of 100)",
            "Apollo": "₹160 (Bottle of 100)"
        }
    },
    "allergy": {
        "issue": "Skin Allergy / Itching",
        "medicine": "Cetirizine 10mg",
        "brands": ["Cetzine", "Okacet"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹12 (Strip of 10)",
            "MedPlus": "₹25 (Strip of 10)",
            "Apollo": "₹30 (Strip of 10)"
        }
    },
     "vomiting": {
        "issue": "Nausea / Vomiting",
        "medicine": "Ondansetron 4mg",
        "brands": ["Emeset 4", "Vomikind 4"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹15 (Strip of 10)",
            "MedPlus": "₹45 (Strip of 10)",
            "Apollo": "₹52 (Strip of 10)"
        }
    },
     "diarrhea": {
        "issue": "Diarrhea / Loose Motion",
        "medicine": "Loperamide 2mg",
        "brands": ["Imodium", "Lopamide"],
        "pricing": {
            "Generic / Jan Aushadhi": "₹15 (Strip of 10)",
            "MedPlus": "₹30 (Strip of 10)",
            "Apollo": "₹35 (Strip of 10)"
        }
    }
}

def get_medicine_suggestions(text_analysis):
    """
    Scans the AI analysis text or user query for keywords and returns 
    rule-based medicine suggestions with pricing comparison.
    """
    found_meds = []
    text_lower = text_analysis.lower()
    
    # Keywords mapping to DB keys
    keywords = {
        "fever": "fever", "temperature": "fever", "pyrexia": "fever",
        "pain": "pain", "headache": "pain", "ache": "pain",
        "acidity": "acidity", "gastritis": "acidity", "heartburn": "acidity", "reflux": "acidity",
        "cold": "cold", "runny nose": "cold", "sneezing": "cold",
        "dry cough": "cough_dry",
        "wet cough": "cough_wet", "phlegm": "cough_wet", "sputum": "cough_wet",
        "infection": "antibiotic", "bacterial": "antibiotic",
        "vitamin d": "vitamin_d", "vit d": "vitamin_d",
        "vitamin b12": "vitamin_b12", "b12": "vitamin_b12",
        "calcium": "calcium", "bones": "calcium",
        "iron": "iron", "hemoglobin": "iron", "anemia": "iron",
        "cholesterol": "cholesterol", "lipid": "cholesterol", "hdl": "cholesterol", "ldl": "cholesterol",
        "sugar": "diabetes", "diabetes": "diabetes", "diabetic": "diabetes", "glucose": "diabetes", "hba1c": "diabetes",
        "blood pressure": "bp", "hypertension": "bp", "bp high": "bp",
        "thyroid": "thyroid", "tsh": "thyroid",
        "allergy": "allergy", "itching": "allergy", "rash": "allergy",
        "vomit": "vomiting", "nausea": "vomiting",
        "diarrhea": "diarrhea", "loose motion": "diarrhea"
    }

    seen_keys = set()
    
    for word, key in keywords.items():
        if word in text_lower and key not in seen_keys:
            if key in MEDICINE_DB:
                found_meds.append(MEDICINE_DB[key])
                seen_keys.add(key)
    
    # Sort for consistent display - unique items
    unique_meds = []
    seen_issues = set()
    for m in found_meds:
        if m['issue'] not in seen_issues:
            unique_meds.append(m)
            seen_issues.add(m['issue'])
            
    return unique_meds

def format_medicine_table(meds):
    if not meds:
        return ""
    
    table_md = "\n\n### 💊 COST-EFFECTIVE MEDICINE OPTIONS (Rule-Based Suggestion)\n\n"
    table_md += "| Health Issue | Medicine (Generic) | Brand Examples | Generic Store (Jan Aushadhi) | MedPlus Price | Apollo Price |\n"
    table_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for m in meds:
        brands = ", ".join(m['brands'])
        p = m['pricing']
        # Escape pipes in strings for markdown table safety
        safe_brands = brands.replace("|", "/")
        safe_med = m['medicine'].replace("|", "/")
        
        row = f"| **{m['issue']}** | {safe_med} | {safe_brands} | 🟢 {p['Generic / Jan Aushadhi']} | {p['MedPlus']} | {p['Apollo']} |\n"
        table_md += row
    
    table_md += "\n\n> *⚠️ Price estimates are for reference. Consult a doctor before taking medication.*"
    return table_md
