import json
import pandas as pd
from typing import Dict, List, Any
import google.generativeai as genai
from datetime import datetime
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AdvancedNephrologyTrainingData:
    """Advanced training data management for enterprise-grade nephrology AI"""
    
    def __init__(self):
        self.clinical_guidelines = self._load_clinical_guidelines()
        self.medical_knowledge_base = self._load_medical_knowledge()
        self.case_studies = self._load_case_studies()
        self.drug_interactions = self._load_drug_interactions()
        self.lab_reference_ranges = self._load_lab_references()
        self.risk_calculators = self._load_risk_calculators()
        
    def _load_clinical_guidelines(self) -> Dict[str, Any]:
        """Load comprehensive clinical guidelines"""
        return {
            "ckd_guidelines": {
                "kdigo_2024": {
                    "stages": {
                        "stage_1": {
                            "gfr": ">= 90",
                            "description": "Normal or high GFR with kidney damage",
                            "management": [
                                "Treat comorbid conditions",
                                "Slow progression of CKD",
                                "Reduce cardiovascular disease risk"
                            ]
                        },
                        "stage_2": {
                            "gfr": "60-89",
                            "description": "Mildly decreased GFR with kidney damage",
                            "management": [
                                "Estimate progression",
                                "Treat comorbid conditions",
                                "Reduce cardiovascular disease risk"
                            ]
                        },
                        "stage_3a": {
                            "gfr": "45-59",
                            "description": "Moderately decreased GFR",
                            "management": [
                                "Evaluate and treat complications",
                                "Prepare for renal replacement therapy"
                            ]
                        },
                        "stage_3b": {
                            "gfr": "30-44",
                            "description": "Moderately to severely decreased GFR",
                            "management": [
                                "Evaluate and treat complications",
                                "Prepare for renal replacement therapy"
                            ]
                        },
                        "stage_4": {
                            "gfr": "15-29",
                            "description": "Severely decreased GFR",
                            "management": [
                                "Prepare for renal replacement therapy",
                                "Consider transplant evaluation"
                            ]
                        },
                        "stage_5": {
                            "gfr": "< 15",
                            "description": "Kidney failure",
                            "management": [
                                "Renal replacement therapy",
                                "Transplant if suitable candidate"
                            ]
                        }
                    }
                },
                "aki_guidelines": {
                    "kdigo_2012": {
                        "stages": {
                            "stage_1": {
                                "creatinine": "1.5-1.9x baseline or ≥0.3 mg/dL increase",
                                "urine_output": "<0.5 mL/kg/h for 6-12h"
                            },
                            "stage_2": {
                                "creatinine": "2.0-2.9x baseline",
                                "urine_output": "<0.5 mL/kg/h for ≥12h"
                            },
                            "stage_3": {
                                "creatinine": "3.0x baseline or ≥4.0 mg/dL or RRT",
                                "urine_output": "<0.3 mL/kg/h for ≥24h or anuria ≥12h"
                            }
                        }
                    }
                }
            },
            "dialysis_guidelines": {
                "hemodialysis": {
                    "adequacy": {
                        "kt_v": ">1.2",
                        "urr": ">65%"
                    },
                    "access": {
                        "preferred": "AV fistula",
                        "alternative": "AV graft",
                        "temporary": "Central venous catheter"
                    }
                },
                "peritoneal_dialysis": {
                    "adequacy": {
                        "weekly_kt_v": ">1.7",
                        "weekly_ccr": ">50L"
                    }
                }
            }
        }
    
    def _load_medical_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive medical knowledge base"""
        return {
            "diseases": {
                "chronic_kidney_disease": {
                    "definition": "Progressive loss of kidney function over time",
                    "causes": [
                        "Diabetes mellitus",
                        "Hypertension",
                        "Glomerulonephritis",
                        "Polycystic kidney disease",
                        "Autoimmune diseases"
                    ],
                    "symptoms": [
                        "Fatigue",
                        "Swelling",
                        "Changes in urination",
                        "Nausea",
                        "Loss of appetite"
                    ],
                    "complications": [
                        "Anemia",
                        "Bone disease",
                        "Cardiovascular disease",
                        "Electrolyte imbalances"
                    ]
                },
                "acute_kidney_injury": {
                    "definition": "Sudden decrease in kidney function",
                    "causes": {
                        "prerenal": ["Dehydration", "Heart failure", "Sepsis"],
                        "intrarenal": ["Acute tubular necrosis", "Glomerulonephritis"],
                        "postrenal": ["Obstruction", "Stones", "Tumors"]
                    },
                    "biomarkers": [
                        "Creatinine",
                        "BUN",
                        "NGAL",
                        "KIM-1",
                        "Cystatin C"
                    ]
                }
            },
            "medications": {
                "ace_inhibitors": {
                    "examples": ["Lisinopril", "Enalapril", "Captopril"],
                    "mechanism": "Block conversion of angiotensin I to II",
                    "nephro_effects": "Reduce proteinuria, slow CKD progression",
                    "contraindications": ["Bilateral renal artery stenosis", "Pregnancy"]
                },
                "arbs": {
                    "examples": ["Losartan", "Valsartan", "Irbesartan"],
                    "mechanism": "Block angiotensin II receptors",
                    "nephro_effects": "Similar to ACE inhibitors"
                }
            }
        }
    
    def _load_case_studies(self) -> List[Dict[str, Any]]:
        """Load clinical case studies for training"""
        return [
            {
                "case_id": "CKD_001",
                "patient": {
                    "age": 65,
                    "gender": "Male",
                    "medical_history": ["Diabetes Type 2", "Hypertension"]
                },
                "presentation": {
                    "chief_complaint": "Fatigue and swelling",
                    "labs": {
                        "creatinine": 2.1,
                        "gfr": 35,
                        "albumin": 3.2,
                        "hemoglobin": 9.8
                    }
                },
                "diagnosis": "CKD Stage 3b",
                "management": [
                    "ACE inhibitor",
                    "Diabetes management",
                    "Anemia treatment",
                    "Nephrology referral"
                ],
                "learning_points": [
                    "Early CKD detection in diabetics",
                    "Importance of proteinuria screening",
                    "Multidisciplinary care approach"
                ]
            },
            {
                "case_id": "AKI_001",
                "patient": {
                    "age": 45,
                    "gender": "Female",
                    "medical_history": ["Lupus"]
                },
                "presentation": {
                    "chief_complaint": "Decreased urine output",
                    "labs": {
                        "creatinine": 3.5,
                        "baseline_creatinine": 1.0,
                        "bun": 45
                    }
                },
                "diagnosis": "AKI Stage 3 - Lupus nephritis",
                "management": [
                    "Immunosuppression",
                    "Fluid management",
                    "Renal biopsy",
                    "Close monitoring"
                ]
            }
        ]
    
    def _load_drug_interactions(self) -> Dict[str, Any]:
        """Load drug interaction database"""
        return {
            "nephrotoxic_drugs": {
                "nsaids": {
                    "examples": ["Ibuprofen", "Naproxen", "Diclofenac"],
                    "mechanism": "Reduce renal blood flow",
                    "risk_factors": ["Dehydration", "Elderly", "CKD"]
                },
                "contrast_agents": {
                    "risk_factors": ["CKD", "Diabetes", "Dehydration"],
                    "prevention": ["Hydration", "N-acetylcysteine", "Minimize dose"]
                },
                "aminoglycosides": {
                    "examples": ["Gentamicin", "Tobramycin"],
                    "monitoring": ["Peak/trough levels", "Creatinine"]
                }
            },
            "dose_adjustments": {
                "gfr_30_60": {
                    "metformin": "Reduce dose by 50%",
                    "gabapentin": "Reduce dose by 50%"
                },
                "gfr_15_30": {
                    "metformin": "Contraindicated",
                    "allopurinol": "Reduce dose by 50%"
                }
            }
        }
    
    def _load_lab_references(self) -> Dict[str, Any]:
        """Load laboratory reference ranges"""
        return {
            "kidney_function": {
                "creatinine": {
                    "male": {"normal": "0.7-1.3 mg/dL", "si_units": "62-115 μmol/L"},
                    "female": {"normal": "0.6-1.1 mg/dL", "si_units": "53-97 μmol/L"}
                },
                "bun": {"normal": "7-20 mg/dL", "si_units": "2.5-7.1 mmol/L"},
                "gfr": {"normal": ">60 mL/min/1.73m²"},
                "cystatin_c": {"normal": "0.5-0.96 mg/L"}
            },
            "electrolytes": {
                "sodium": {"normal": "136-145 mEq/L"},
                "potassium": {"normal": "3.5-5.0 mEq/L"},
                "chloride": {"normal": "98-107 mEq/L"},
                "co2": {"normal": "22-28 mEq/L"}
            },
            "minerals": {
                "calcium": {"normal": "8.5-10.5 mg/dL"},
                "phosphorus": {"normal": "2.5-4.5 mg/dL"},
                "magnesium": {"normal": "1.7-2.2 mg/dL"}
            }
        }
    
    def _load_risk_calculators(self) -> Dict[str, Any]:
        """Load risk calculation formulas"""
        return {
            "gfr_equations": {
                "ckd_epi_2021": {
                    "formula": "142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^-1.200 × 0.9938^age × (1.012 if female)",
                    "variables": {
                        "Scr": "Serum creatinine (mg/dL)",
                        "κ": "0.7 (female) or 0.9 (male)",
                        "α": "-0.241 (female) or -0.302 (male)"
                    }
                },
                "mdrd": {
                    "formula": "175 × (Scr)^-1.154 × (Age)^-0.203 × (0.742 if female) × (1.212 if African American)"
                }
            },
            "cardiovascular_risk": {
                "ckd_cv_risk": {
                    "factors": ["GFR", "Albuminuria", "Age", "Diabetes", "Hypertension"],
                    "categories": {
                        "low": "GFR >60, no albuminuria",
                        "moderate": "GFR 30-60 or albuminuria",
                        "high": "GFR <30 or severe albuminuria"
                    }
                }
            },
            "progression_risk": {
                "kidney_failure_risk_equation": {
                    "variables": ["Age", "Sex", "eGFR", "Albumin-to-creatinine ratio"],
                    "outcomes": "2-year and 5-year risk of kidney failure"
                }
            }
        }
    
    def get_clinical_recommendation(self, condition: str, stage: str = None) -> Dict[str, Any]:
        """Get clinical recommendations based on condition and stage"""
        if condition.lower() == "ckd" and stage:
            return self.clinical_guidelines["ckd_guidelines"]["kdigo_2024"]["stages"].get(stage, {})
        elif condition.lower() == "aki" and stage:
            return self.clinical_guidelines["ckd_guidelines"]["aki_guidelines"]["kdigo_2012"]["stages"].get(stage, {})
        return {}
    
    def calculate_gfr(self, creatinine: float, age: int, gender: str, race: str = "other") -> float:
        """Calculate GFR using CKD-EPI 2021 equation"""
        # Simplified CKD-EPI calculation
        if gender.lower() == "female":
            kappa = 0.7
            alpha = -0.241
            gender_factor = 1.012
        else:
            kappa = 0.9
            alpha = -0.302
            gender_factor = 1.0
        
        min_scr_kappa = min(creatinine / kappa, 1)
        max_scr_kappa = max(creatinine / kappa, 1)
        
        gfr = (142 * (min_scr_kappa ** alpha) * (max_scr_kappa ** -1.200) * 
               (0.9938 ** age) * gender_factor)
        
        return round(gfr, 1)
    
    def get_drug_adjustment(self, drug: str, gfr: float) -> str:
        """Get drug dosing adjustment based on GFR"""
        adjustments = self.drug_interactions["dose_adjustments"]
        
        if gfr < 15:
            return f"{drug}: Contraindicated or requires dialysis dosing"
        elif gfr < 30:
            if "gfr_15_30" in adjustments and drug.lower() in adjustments["gfr_15_30"]:
                return adjustments["gfr_15_30"][drug.lower()]
        elif gfr < 60:
            if "gfr_30_60" in adjustments and drug.lower() in adjustments["gfr_30_60"]:
                return adjustments["gfr_30_60"][drug.lower()]
        
        return "No adjustment needed"
    
    def generate_training_prompt(self, case_type: str = "general") -> str:
        """Generate comprehensive training prompts for the AI model"""
        base_prompt = """
You are an advanced nephrology AI assistant with enterprise-grade capabilities. You have access to:

1. Latest clinical guidelines (KDIGO 2024, NKF, ASN)
2. Comprehensive drug interaction database
3. Risk calculation tools
4. Evidence-based treatment protocols
5. Clinical case studies and best practices

Your responses should be:
- Clinically accurate and evidence-based
- Appropriately cautious with medical advice
- Comprehensive yet accessible
- Include relevant risk factors and contraindications
- Suggest appropriate follow-up and monitoring

Always remind users that your recommendations are for educational purposes and should not replace professional medical consultation.
"""
        
        if case_type == "ckd":
            base_prompt += """

Special focus on CKD management:
- Stage-appropriate interventions
- Progression risk assessment
- Complication management (anemia, bone disease, CV risk)
- Preparation for renal replacement therapy
- Patient education and lifestyle modifications
"""
        elif case_type == "aki":
            base_prompt += """

Special focus on AKI management:
- Rapid assessment and staging
- Cause identification (prerenal, intrarenal, postrenal)
- Nephrotoxin avoidance
- Fluid and electrolyte management
- Recovery monitoring
"""
        
        return base_prompt
    
    def get_enhanced_context(self, query: str) -> str:
        """Get enhanced context for AI responses"""
        # Simple keyword matching for demonstration
        context = ""
        
        if "ckd" in query.lower() or "chronic kidney" in query.lower():
            context += "\n\nCKD Context:\n"
            context += json.dumps(self.clinical_guidelines["ckd_guidelines"]["kdigo_2024"], indent=2)
        
        if "aki" in query.lower() or "acute kidney" in query.lower():
            context += "\n\nAKI Context:\n"
            context += json.dumps(self.clinical_guidelines["ckd_guidelines"]["aki_guidelines"], indent=2)
        
        if "drug" in query.lower() or "medication" in query.lower():
            context += "\n\nDrug Information:\n"
            context += json.dumps(self.drug_interactions, indent=2)
        
        return context

# Initialize the advanced training data
advanced_training = AdvancedNephrologyTrainingData()