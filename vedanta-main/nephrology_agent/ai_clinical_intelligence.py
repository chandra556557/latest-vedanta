import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import sqlite3
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class KidneyFunctionPredictor:
    """Advanced ML model for kidney function prediction using GFR trends and biomarkers"""
    
    def __init__(self):
        self.gfr_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.progression_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, patient_data):
        """Prepare features for ML models"""
        features = []
        
        # Basic demographics
        features.extend([
            patient_data.get('age', 0),
            1 if patient_data.get('gender') == 'male' else 0,
            patient_data.get('bmi', 25)
        ])
        
        # Lab values
        features.extend([
            patient_data.get('creatinine', 1.0),
            patient_data.get('bun', 20),
            patient_data.get('albumin', 4.0),
            patient_data.get('hemoglobin', 12.0),
            patient_data.get('phosphorus', 3.5),
            patient_data.get('calcium', 9.5),
            patient_data.get('pth', 50)
        ])
        
        # Comorbidities (binary)
        features.extend([
            1 if patient_data.get('diabetes') else 0,
            1 if patient_data.get('hypertension') else 0,
            1 if patient_data.get('cardiovascular_disease') else 0,
            1 if patient_data.get('proteinuria') else 0
        ])
        
        # Medications (binary)
        features.extend([
            1 if patient_data.get('ace_inhibitor') else 0,
            1 if patient_data.get('arb') else 0,
            1 if patient_data.get('diuretic') else 0
        ])
        
        return np.array(features).reshape(1, -1)
    
    def predict_gfr(self, patient_data):
        """Predict future GFR based on current data"""
        if not self.is_trained:
            self._train_models()
            
        features = self.prepare_features(patient_data)
        features_scaled = self.scaler.transform(features)
        
        predicted_gfr = self.gfr_model.predict(features_scaled)[0]
        confidence = self.gfr_model.score(features_scaled, [predicted_gfr])
        
        return {
            'predicted_gfr': round(predicted_gfr, 2),
            'confidence': round(confidence * 100, 2),
            'stage': self._classify_ckd_stage(predicted_gfr)
        }
    
    def predict_progression_risk(self, patient_data):
        """Predict risk of CKD progression"""
        if not self.is_trained:
            self._train_models()
            
        features = self.prepare_features(patient_data)
        features_scaled = self.scaler.transform(features)
        
        risk_prob = self.progression_model.predict_proba(features_scaled)[0][1]
        risk_level = 'Low' if risk_prob < 0.3 else 'Moderate' if risk_prob < 0.7 else 'High'
        
        return {
            'progression_risk': round(risk_prob * 100, 2),
            'risk_level': risk_level,
            'factors': self._identify_risk_factors(patient_data)
        }
    
    def _classify_ckd_stage(self, gfr):
        """Classify CKD stage based on GFR"""
        if gfr >= 90:
            return 'Stage 1 (Normal or high)'
        elif gfr >= 60:
            return 'Stage 2 (Mildly decreased)'
        elif gfr >= 45:
            return 'Stage 3a (Moderately decreased)'
        elif gfr >= 30:
            return 'Stage 3b (Moderately decreased)'
        elif gfr >= 15:
            return 'Stage 4 (Severely decreased)'
        else:
            return 'Stage 5 (Kidney failure)'
    
    def _identify_risk_factors(self, patient_data):
        """Identify key risk factors for progression"""
        factors = []
        
        if patient_data.get('diabetes'):
            factors.append('Diabetes mellitus')
        if patient_data.get('hypertension'):
            factors.append('Hypertension')
        if patient_data.get('proteinuria'):
            factors.append('Proteinuria')
        if patient_data.get('creatinine', 1.0) > 1.5:
            factors.append('Elevated creatinine')
        if patient_data.get('age', 0) > 65:
            factors.append('Advanced age')
            
        return factors
    
    def _train_models(self):
        """Train ML models with synthetic data (in production, use real data)"""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        
        # Features: age, gender, bmi, creatinine, bun, albumin, hemoglobin, phosphorus, calcium, pth, diabetes, hypertension, cvd, proteinuria, ace_inhibitor, arb, diuretic
        X = np.random.rand(n_samples, 17)
        
        # Simulate realistic ranges
        X[:, 0] = X[:, 0] * 60 + 20  # age 20-80
        X[:, 1] = (X[:, 1] > 0.5).astype(int)  # gender binary
        X[:, 2] = X[:, 2] * 15 + 18  # BMI 18-33
        X[:, 3] = X[:, 3] * 3 + 0.5  # creatinine 0.5-3.5
        X[:, 4] = X[:, 4] * 50 + 10  # BUN 10-60
        X[:, 5] = X[:, 5] * 2 + 3  # albumin 3-5
        X[:, 6] = X[:, 6] * 6 + 8  # hemoglobin 8-14
        X[:, 7] = X[:, 7] * 3 + 2  # phosphorus 2-5
        X[:, 8] = X[:, 8] * 3 + 8  # calcium 8-11
        X[:, 9] = X[:, 9] * 200 + 10  # PTH 10-210
        
        # Binary features
        for i in range(10, 17):
            X[:, i] = (X[:, i] > 0.5).astype(int)
        
        # Generate target variables
        # GFR prediction (simplified relationship)
        y_gfr = 120 - (X[:, 3] * 30) - (X[:, 0] * 0.5) + np.random.normal(0, 5, n_samples)
        y_gfr = np.clip(y_gfr, 5, 120)
        
        # Progression risk (binary)
        progression_score = (X[:, 3] * 0.3) + (X[:, 10] * 0.2) + (X[:, 11] * 0.15) + (X[:, 13] * 0.25)
        y_progression = (progression_score > np.median(progression_score)).astype(int)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        self.gfr_model.fit(X_scaled, y_gfr)
        self.progression_model.fit(X_scaled, y_progression)
        
        self.is_trained = True

class ClinicalDecisionSupport:
    """Evidence-based clinical decision support system"""
    
    def __init__(self):
        self.guidelines = self._load_clinical_guidelines()
    
    def get_treatment_recommendations(self, patient_data, gfr_prediction):
        """Get evidence-based treatment recommendations"""
        recommendations = []
        
        current_gfr = patient_data.get('current_gfr', gfr_prediction.get('predicted_gfr', 60))
        stage = gfr_prediction.get('stage', 'Unknown')
        
        # Blood pressure management
        if patient_data.get('hypertension') or patient_data.get('systolic_bp', 120) > 130:
            recommendations.append({
                'category': 'Blood Pressure Management',
                'recommendation': 'Target BP <130/80 mmHg. Consider ACE inhibitor or ARB if not contraindicated.',
                'evidence_level': 'A',
                'priority': 'High'
            })
        
        # Diabetes management
        if patient_data.get('diabetes') or patient_data.get('hba1c', 5.5) > 7.0:
            recommendations.append({
                'category': 'Diabetes Management',
                'recommendation': 'Target HbA1c <7% (or individualized target). Consider SGLT2 inhibitors for cardio-renal protection.',
                'evidence_level': 'A',
                'priority': 'High'
            })
        
        # Proteinuria management
        if patient_data.get('proteinuria') or patient_data.get('uacr', 0) > 30:
            recommendations.append({
                'category': 'Proteinuria Management',
                'recommendation': 'Optimize ACE inhibitor/ARB therapy. Consider mineralocorticoid receptor antagonist.',
                'evidence_level': 'A',
                'priority': 'High'
            })
        
        # Mineral bone disorder
        if current_gfr < 45:
            recommendations.append({
                'category': 'Mineral Bone Disorder',
                'recommendation': 'Monitor calcium, phosphorus, PTH, and vitamin D. Consider phosphate binders if needed.',
                'evidence_level': 'B',
                'priority': 'Moderate'
            })
        
        # Anemia management
        if patient_data.get('hemoglobin', 12) < 10 and current_gfr < 30:
            recommendations.append({
                'category': 'Anemia Management',
                'recommendation': 'Evaluate iron status. Consider ESA therapy if iron replete and Hgb <10 g/dL.',
                'evidence_level': 'B',
                'priority': 'Moderate'
            })
        
        # Cardiovascular risk
        if patient_data.get('cardiovascular_disease') or current_gfr < 60:
            recommendations.append({
                'category': 'Cardiovascular Risk',
                'recommendation': 'Consider statin therapy. Optimize cardiovascular risk factors.',
                'evidence_level': 'A',
                'priority': 'High'
            })
        
        # Nephrology referral
        if current_gfr < 30 or (current_gfr < 45 and gfr_prediction.get('progression_risk', 0) > 50):
            recommendations.append({
                'category': 'Specialist Referral',
                'recommendation': 'Refer to nephrology for advanced CKD management and renal replacement therapy planning.',
                'evidence_level': 'A',
                'priority': 'High'
            })
        
        return recommendations
    
    def get_drug_dosing_recommendations(self, patient_data, medications):
        """Get kidney function-based drug dosing recommendations"""
        current_gfr = patient_data.get('current_gfr', 60)
        recommendations = []
        
        dosing_adjustments = {
            'metformin': {
                'gfr_threshold': 30,
                'recommendation': 'Discontinue if GFR <30 mL/min/1.73m²'
            },
            'gabapentin': {
                'gfr_threshold': 60,
                'recommendation': 'Reduce dose by 50% if GFR 30-60, by 75% if GFR 15-30'
            },
            'allopurinol': {
                'gfr_threshold': 60,
                'recommendation': 'Reduce starting dose to 100mg daily if GFR <60'
            },
            'digoxin': {
                'gfr_threshold': 50,
                'recommendation': 'Reduce dose by 25-50% and monitor levels closely'
            }
        }
        
        for medication in medications:
            med_name = medication.lower()
            if med_name in dosing_adjustments:
                adjustment = dosing_adjustments[med_name]
                if current_gfr < adjustment['gfr_threshold']:
                    recommendations.append({
                        'medication': medication,
                        'current_gfr': current_gfr,
                        'recommendation': adjustment['recommendation'],
                        'priority': 'High' if 'discontinue' in adjustment['recommendation'].lower() else 'Moderate'
                    })
        
        return recommendations
    
    def _load_clinical_guidelines(self):
        """Load clinical guidelines and evidence-based recommendations"""
        return {
            'ckd_stages': {
                1: 'Normal or high GFR (≥90) with kidney damage',
                2: 'Mildly decreased GFR (60-89) with kidney damage',
                3: 'Moderately decreased GFR (30-59)',
                4: 'Severely decreased GFR (15-29)',
                5: 'Kidney failure (GFR <15 or on dialysis)'
            },
            'bp_targets': {
                'general': '<130/80 mmHg',
                'diabetes': '<130/80 mmHg',
                'proteinuria': '<130/80 mmHg'
            },
            'monitoring_frequency': {
                'stage_1_2': 'Annual',
                'stage_3a': 'Every 6 months',
                'stage_3b_4': 'Every 3-6 months',
                'stage_5': 'Monthly'
            }
        }

class IntelligentAlerts:
    """Intelligent alert system for critical lab values and trends"""
    
    def __init__(self):
        self.alert_thresholds = self._define_alert_thresholds()
    
    def check_critical_values(self, lab_data):
        """Check for critical lab values requiring immediate attention"""
        alerts = []
        
        for lab, value in lab_data.items():
            if lab in self.alert_thresholds:
                thresholds = self.alert_thresholds[lab]
                
                if value < thresholds['critical_low']:
                    alerts.append({
                        'type': 'Critical Low',
                        'lab': lab,
                        'value': value,
                        'threshold': thresholds['critical_low'],
                        'urgency': 'Critical',
                        'action': thresholds['action_low']
                    })
                elif value > thresholds['critical_high']:
                    alerts.append({
                        'type': 'Critical High',
                        'lab': lab,
                        'value': value,
                        'threshold': thresholds['critical_high'],
                        'urgency': 'Critical',
                        'action': thresholds['action_high']
                    })
                elif value < thresholds['warning_low'] or value > thresholds['warning_high']:
                    alerts.append({
                        'type': 'Warning',
                        'lab': lab,
                        'value': value,
                        'urgency': 'Warning',
                        'action': 'Monitor closely and consider intervention'
                    })
        
        return alerts
    
    def analyze_trends(self, historical_data):
        """Analyze lab value trends for early warning signs"""
        trend_alerts = []
        
        for lab, values in historical_data.items():
            if len(values) >= 3:
                # Calculate trend
                recent_values = values[-3:]
                trend = np.polyfit(range(len(recent_values)), recent_values, 1)[0]
                
                # Check for concerning trends
                if lab == 'creatinine' and trend > 0.2:  # Rising creatinine
                    trend_alerts.append({
                        'type': 'Trend Alert',
                        'lab': lab,
                        'trend': 'Increasing',
                        'rate': round(trend, 3),
                        'concern': 'Declining kidney function',
                        'urgency': 'High'
                    })
                elif lab == 'gfr' and trend < -5:  # Declining GFR
                    trend_alerts.append({
                        'type': 'Trend Alert',
                        'lab': lab,
                        'trend': 'Decreasing',
                        'rate': round(abs(trend), 1),
                        'concern': 'Progressive CKD',
                        'urgency': 'High'
                    })
                elif lab == 'proteinuria' and trend > 50:  # Increasing proteinuria
                    trend_alerts.append({
                        'type': 'Trend Alert',
                        'lab': lab,
                        'trend': 'Increasing',
                        'rate': round(trend, 1),
                        'concern': 'Progressive kidney damage',
                        'urgency': 'Moderate'
                    })
        
        return trend_alerts
    
    def _define_alert_thresholds(self):
        """Define critical and warning thresholds for lab values"""
        return {
            'creatinine': {
                'critical_low': 0.3,
                'warning_low': 0.5,
                'warning_high': 2.0,
                'critical_high': 4.0,
                'action_low': 'Check for measurement error or muscle wasting',
                'action_high': 'Immediate nephrology consultation, check for AKI'
            },
            'potassium': {
                'critical_low': 2.5,
                'warning_low': 3.0,
                'warning_high': 5.5,
                'critical_high': 6.5,
                'action_low': 'Potassium replacement, monitor cardiac rhythm',
                'action_high': 'Emergency treatment, cardiac monitoring'
            },
            'hemoglobin': {
                'critical_low': 6.0,
                'warning_low': 8.0,
                'warning_high': 16.0,
                'critical_high': 18.0,
                'action_low': 'Consider transfusion, investigate cause',
                'action_high': 'Investigate polycythemia, consider phlebotomy'
            },
            'calcium': {
                'critical_low': 7.0,
                'warning_low': 8.0,
                'warning_high': 11.0,
                'critical_high': 13.0,
                'action_low': 'Calcium replacement, monitor for tetany',
                'action_high': 'Immediate treatment, investigate cause'
            }
        }

class DialysisReadinessPredictor:
    """Predicts dialysis readiness and optimal timing based on clinical parameters"""
    
    def predict_dialysis_timing(self, patient_data, lab_data=None, symptoms=None):
        """Predict when patient may need dialysis initiation"""
        try:
            gfr = patient_data.get('current_gfr', 0)
            creatinine = patient_data.get('creatinine', 0)
            symptoms = symptoms or []
            
            # Calculate dialysis readiness score
            readiness_score = 0
            urgency = "Low"
            
            # GFR-based scoring
            if gfr <= 10:
                readiness_score += 40
                urgency = "Critical"
            elif gfr <= 15:
                readiness_score += 30
                urgency = "High"
            elif gfr <= 20:
                readiness_score += 20
                urgency = "Moderate"
            
            # Symptom-based scoring
            high_risk_symptoms = ['fluid_overload', 'uremic_symptoms', 'severe_acidosis', 'hyperkalemia']
            for symptom in symptoms:
                if symptom in high_risk_symptoms:
                    readiness_score += 15
            
            # Lab-based indicators
            if lab_data:
                if lab_data.get('potassium', 0) > 6.0:
                    readiness_score += 20
                if lab_data.get('phosphorus', 0) > 7.0:
                    readiness_score += 10
            
            # Predicted timeline
            if readiness_score >= 70:
                timeline = "Immediate (within 1-2 weeks)"
            elif readiness_score >= 50:
                timeline = "Short-term (1-3 months)"
            elif readiness_score >= 30:
                timeline = "Medium-term (3-6 months)"
            else:
                timeline = "Long-term (>6 months)"
            
            return {
                'readiness_score': min(readiness_score, 100),
                'urgency': urgency,
                'predicted_timeline': timeline,
                'current_gfr': gfr,
                'recommendations': self._get_dialysis_preparation_recommendations(readiness_score, gfr)
            }
            
        except Exception as e:
            return {'error': f"Dialysis prediction failed: {str(e)}"}
    
    def _get_dialysis_preparation_recommendations(self, score, gfr):
        """Get recommendations for dialysis preparation"""
        recommendations = []
        
        if score >= 50:
            recommendations.extend([
                "Urgent nephrology consultation for dialysis planning",
                "Vascular access evaluation and creation",
                "Patient education on dialysis modalities",
                "Nutritional counseling for dialysis preparation"
            ])
        elif score >= 30:
            recommendations.extend([
                "Nephrology follow-up within 1-2 months",
                "Consider vascular access planning",
                "Begin dialysis education",
                "Optimize medical management"
            ])
        else:
            recommendations.extend([
                "Regular nephrology monitoring",
                "Continue conservative management",
                "Lifestyle modifications",
                "Monitor for progression"
            ])
        
        return recommendations

class TransplantReadinessAnalyzer:
    """Analyzes transplant eligibility and readiness"""
    
    def analyze_transplant_eligibility(self, patient_data, lab_data=None, comorbidities=None):
        """Analyze patient's eligibility for kidney transplantation"""
        try:
            age = patient_data.get('age', 0)
            gfr = patient_data.get('current_gfr', 0)
            comorbidities = comorbidities or []
            
            eligibility_score = 100
            contraindications = []
            recommendations = []
            
            # Age considerations
            if age > 75:
                eligibility_score -= 30
                contraindications.append("Advanced age (>75 years)")
            elif age > 65:
                eligibility_score -= 15
                recommendations.append("Age consideration - enhanced evaluation needed")
            
            # GFR considerations
            if gfr > 20:
                recommendations.append("GFR still adequate - monitor for decline")
            elif gfr <= 15:
                recommendations.append("Appropriate GFR for transplant evaluation")
            
            # Comorbidity assessment
            high_risk_comorbidities = [
                'active_cancer', 'severe_heart_disease', 'severe_lung_disease',
                'active_substance_abuse', 'severe_psychiatric_illness'
            ]
            
            for condition in comorbidities:
                if condition in high_risk_comorbidities:
                    eligibility_score -= 40
                    contraindications.append(f"High-risk comorbidity: {condition}")
            
            # Determine eligibility status
            if eligibility_score >= 80:
                status = "Excellent candidate"
            elif eligibility_score >= 60:
                status = "Good candidate"
            elif eligibility_score >= 40:
                status = "Marginal candidate - needs evaluation"
            else:
                status = "Poor candidate - significant contraindications"
            
            # Timeline recommendations
            if gfr <= 20 and eligibility_score >= 60:
                timeline = "Begin evaluation process now"
            elif gfr <= 25 and eligibility_score >= 60:
                timeline = "Consider evaluation within 6 months"
            else:
                timeline = "Continue monitoring"
            
            return {
                'eligibility_score': eligibility_score,
                'status': status,
                'timeline': timeline,
                'contraindications': contraindications,
                'recommendations': recommendations,
                'next_steps': self._get_transplant_next_steps(eligibility_score, gfr)
            }
            
        except Exception as e:
            return {'error': f"Transplant analysis failed: {str(e)}"}
    
    def _get_transplant_next_steps(self, score, gfr):
        """Get next steps for transplant evaluation"""
        steps = []
        
        if score >= 60 and gfr <= 20:
            steps.extend([
                "Referral to transplant center",
                "Complete medical evaluation",
                "Psychosocial assessment",
                "Living donor evaluation if available",
                "Waitlist registration"
            ])
        elif score >= 40:
            steps.extend([
                "Nephrology consultation",
                "Address modifiable risk factors",
                "Optimize medical management",
                "Consider transplant education"
            ])
        else:
            steps.extend([
                "Focus on conservative management",
                "Address contraindications",
                "Regular monitoring",
                "Reassess eligibility periodically"
            ])
        
        return steps

class DrugDosingRecommendations:
    """AI-powered drug dosing recommendations based on kidney function"""
    
    def __init__(self):
        self.drug_database = {
            'metformin': {
                'normal_dose': '500-1000mg BID',
                'gfr_adjustments': {
                    60: '500mg BID',
                    45: '500mg daily',
                    30: 'Contraindicated'
                },
                'monitoring': 'GFR, lactic acid'
            },
            'atenolol': {
                'normal_dose': '25-100mg daily',
                'gfr_adjustments': {
                    50: '50% dose reduction',
                    35: '75% dose reduction',
                    15: 'Avoid or use alternative'
                },
                'monitoring': 'Heart rate, blood pressure'
            },
            'lisinopril': {
                'normal_dose': '5-40mg daily',
                'gfr_adjustments': {
                    60: 'Standard dose',
                    30: 'Start low, monitor closely',
                    15: 'Use with extreme caution'
                },
                'monitoring': 'GFR, potassium, blood pressure'
            },
            'gabapentin': {
                'normal_dose': '300-1200mg TID',
                'gfr_adjustments': {
                    60: '300-600mg TID',
                    30: '200-400mg BID',
                    15: '100-200mg daily'
                },
                'monitoring': 'Neurological symptoms, GFR'
            },
            'allopurinol': {
                'normal_dose': '100-300mg daily',
                'gfr_adjustments': {
                    60: '200mg daily',
                    30: '100mg daily',
                    15: '100mg every other day'
                },
                'monitoring': 'Uric acid, liver function, GFR'
            }
        }
    
    def get_dosing_recommendations(self, patient_data, medications, lab_data=None):
        """Get AI-powered drug dosing recommendations"""
        try:
            gfr = patient_data.get('current_gfr', 100)
            age = patient_data.get('age', 0)
            weight = patient_data.get('weight', 70)
            
            recommendations = []
            
            for medication in medications:
                med_name = medication.lower()
                if med_name in self.drug_database:
                    rec = self._calculate_dose_adjustment(
                        med_name, gfr, age, weight, lab_data
                    )
                    recommendations.append(rec)
            
            return {
                'recommendations': recommendations,
                'general_principles': self._get_general_principles(gfr),
                'monitoring_schedule': self._get_monitoring_schedule(gfr, medications)
            }
            
        except Exception as e:
            return {'error': f"Drug dosing analysis failed: {str(e)}"}
    
    def _calculate_dose_adjustment(self, medication, gfr, age, weight, lab_data):
        """Calculate dose adjustment for specific medication"""
        drug_info = self.drug_database[medication]
        
        # Find appropriate GFR threshold
        adjusted_dose = drug_info['normal_dose']
        risk_level = 'Low'
        
        for threshold in sorted(drug_info['gfr_adjustments'].keys(), reverse=True):
            if gfr <= threshold:
                adjusted_dose = drug_info['gfr_adjustments'][threshold]
                if 'Contraindicated' in adjusted_dose or 'Avoid' in adjusted_dose:
                    risk_level = 'High'
                elif 'caution' in adjusted_dose.lower():
                    risk_level = 'Moderate'
                break
        
        # Age-based adjustments
        age_adjustment = ""
        if age > 65:
            age_adjustment = "Consider additional 25% dose reduction due to age"
        
        return {
            'medication': medication.title(),
            'normal_dose': drug_info['normal_dose'],
            'recommended_dose': adjusted_dose,
            'age_adjustment': age_adjustment,
            'monitoring': drug_info['monitoring'],
            'risk_level': risk_level,
            'rationale': f"Adjusted for GFR {gfr} mL/min/1.73m²"
        }
    
    def _get_general_principles(self, gfr):
        """Get general dosing principles based on GFR"""
        if gfr >= 60:
            return [
                "Standard dosing for most medications",
                "Monitor nephrotoxic drugs closely",
                "Regular GFR monitoring recommended"
            ]
        elif gfr >= 30:
            return [
                "Dose adjustments required for many medications",
                "Avoid nephrotoxic drugs when possible",
                "Frequent monitoring of kidney function",
                "Consider alternative medications"
            ]
        else:
            return [
                "Significant dose reductions required",
                "Many medications contraindicated",
                "Specialist consultation recommended",
                "Prepare for renal replacement therapy"
            ]
    
    def _get_monitoring_schedule(self, gfr, medications):
        """Get recommended monitoring schedule"""
        if gfr >= 60:
            return "Monitor GFR every 6-12 months"
        elif gfr >= 30:
            return "Monitor GFR every 3-6 months"
        else:
            return "Monitor GFR monthly or as clinically indicated"

class ClinicalNotesNLP:
    """Natural Language Processing for clinical notes analysis"""
    
    def __init__(self):
        self.medical_keywords = {
            'symptoms': ['pain', 'swelling', 'fatigue', 'nausea', 'vomiting', 'shortness of breath', 'chest pain'],
            'conditions': ['diabetes', 'hypertension', 'ckd', 'kidney disease', 'proteinuria', 'hematuria'],
            'medications': ['lisinopril', 'metformin', 'furosemide', 'atenolol', 'amlodipine'],
            'lab_values': ['creatinine', 'gfr', 'bun', 'albumin', 'hemoglobin', 'potassium'],
            'urgency_indicators': ['urgent', 'emergency', 'critical', 'severe', 'acute', 'immediate']
        }
        
        self.severity_scores = {
            'mild': 1, 'moderate': 2, 'severe': 3, 'critical': 4,
            'low': 1, 'medium': 2, 'high': 3, 'urgent': 4
        }
    
    def analyze_clinical_notes(self, notes_text, patient_data=None):
        """Comprehensive analysis of clinical notes"""
        try:
            if not notes_text or not notes_text.strip():
                return {'error': 'No clinical notes provided'}
            
            # Extract key information
            extracted_info = self._extract_medical_entities(notes_text)
            sentiment_analysis = self._analyze_clinical_sentiment(notes_text)
            risk_indicators = self._identify_risk_indicators(notes_text)
            recommendations = self._generate_note_recommendations(extracted_info, risk_indicators)
            
            return {
                'extracted_entities': extracted_info,
                'clinical_sentiment': sentiment_analysis,
                'risk_indicators': risk_indicators,
                'recommendations': recommendations,
                'summary': self._generate_clinical_summary(extracted_info, sentiment_analysis)
            }
            
        except Exception as e:
            return {'error': f"Clinical notes analysis failed: {str(e)}"}
    
    def _extract_medical_entities(self, text):
        """Extract medical entities from clinical notes"""
        text_lower = text.lower()
        entities = {
            'symptoms': [],
            'conditions': [],
            'medications': [],
            'lab_values': [],
            'procedures': []
        }
        
        # Extract symptoms
        for symptom in self.medical_keywords['symptoms']:
            if symptom in text_lower:
                entities['symptoms'].append(symptom.title())
        
        # Extract conditions
        for condition in self.medical_keywords['conditions']:
            if condition in text_lower:
                entities['conditions'].append(condition.upper() if condition == 'ckd' else condition.title())
        
        # Extract medications
        for medication in self.medical_keywords['medications']:
            if medication in text_lower:
                entities['medications'].append(medication.title())
        
        # Extract lab values mentions
        for lab in self.medical_keywords['lab_values']:
            if lab in text_lower:
                entities['lab_values'].append(lab.upper() if lab in ['gfr', 'bun'] else lab.title())
        
        return entities
    
    def _analyze_clinical_sentiment(self, text):
        """Analyze clinical sentiment and urgency"""
        text_lower = text.lower()
        
        # Count positive and negative indicators
        positive_words = ['stable', 'improved', 'better', 'normal', 'good', 'excellent']
        negative_words = ['worse', 'deteriorated', 'poor', 'abnormal', 'concerning', 'critical']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Determine overall sentiment
        if negative_count > positive_count:
            sentiment = 'Concerning'
            urgency = 'High'
        elif positive_count > negative_count:
            sentiment = 'Stable/Improving'
            urgency = 'Low'
        else:
            sentiment = 'Neutral'
            urgency = 'Medium'
        
        return {
            'overall_sentiment': sentiment,
            'urgency_level': urgency,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count
        }
    
    def _identify_risk_indicators(self, text):
        """Identify clinical risk indicators"""
        text_lower = text.lower()
        risk_indicators = []
        
        # Check for urgency indicators
        for indicator in self.medical_keywords['urgency_indicators']:
            if indicator in text_lower:
                risk_indicators.append({
                    'type': 'Urgency',
                    'indicator': indicator.title(),
                    'severity': 'High'
                })
        
        # Check for specific nephrology risks
        nephro_risks = {
            'rapid decline': 'GFR decline',
            'fluid overload': 'Volume management',
            'hyperkalemia': 'Electrolyte imbalance',
            'metabolic acidosis': 'Acid-base disorder',
            'bone disease': 'CKD-MBD'
        }
        
        for risk_phrase, risk_type in nephro_risks.items():
            if risk_phrase in text_lower:
                risk_indicators.append({
                    'type': 'Clinical Risk',
                    'indicator': risk_type,
                    'severity': 'Medium'
                })
        
        return risk_indicators
    
    def _generate_note_recommendations(self, entities, risk_indicators):
        """Generate recommendations based on note analysis"""
        recommendations = []
        
        # Medication-based recommendations
        if entities['medications']:
            recommendations.append("Review current medications for kidney function adjustments")
        
        # Symptom-based recommendations
        if 'Shortness Of Breath' in entities['symptoms'] or 'Swelling' in entities['symptoms']:
            recommendations.append("Assess fluid status and consider diuretic adjustment")
        
        # Risk-based recommendations
        high_risk_count = sum(1 for risk in risk_indicators if risk['severity'] == 'High')
        if high_risk_count > 0:
            recommendations.append("Consider urgent nephrology consultation")
            recommendations.append("Monitor closely with frequent lab checks")
        
        # Lab-based recommendations
        if entities['lab_values']:
            recommendations.append("Review recent lab trends and compare with historical values")
        
        return recommendations if recommendations else ["Continue current management plan"]
    
    def _generate_clinical_summary(self, entities, sentiment):
        """Generate a clinical summary"""
        summary_parts = []
        
        # Add condition summary
        if entities['conditions']:
            summary_parts.append(f"Conditions noted: {', '.join(entities['conditions'])}")
        
        # Add symptom summary
        if entities['symptoms']:
            summary_parts.append(f"Symptoms reported: {', '.join(entities['symptoms'])}")
        
        # Add sentiment
        summary_parts.append(f"Clinical status: {sentiment['overall_sentiment']}")
        
        return '. '.join(summary_parts) if summary_parts else "No significant clinical findings extracted"


class IntelligentAlerts:
    """Intelligent alert system for critical lab values and trends"""
    
    def __init__(self):
        # Critical value thresholds
        self.critical_thresholds = {
            'creatinine': {'critical': 4.0, 'severe': 3.0, 'moderate': 2.5},
            'gfr': {'critical': 15, 'severe': 20, 'moderate': 30},
            'potassium': {'critical_high': 6.0, 'critical_low': 2.5, 'severe_high': 5.5, 'severe_low': 3.0},
            'hemoglobin': {'critical': 7.0, 'severe': 8.0, 'moderate': 9.0},
            'albumin': {'critical': 2.0, 'severe': 2.5, 'moderate': 3.0},
            'phosphorus': {'critical_high': 7.0, 'severe_high': 6.0, 'moderate_high': 5.5},
            'calcium': {'critical_low': 7.0, 'critical_high': 12.0, 'severe_low': 7.5, 'severe_high': 11.5},
            'bun': {'critical': 100, 'severe': 80, 'moderate': 60}
        }
        
        # Trend analysis parameters
        self.trend_thresholds = {
            'rapid_decline': 0.3,  # 30% decline in GFR
            'concerning_trend': 0.2,  # 20% decline
            'stable_threshold': 0.1   # 10% variation
        }
    
    def analyze_critical_values(self, lab_data, patient_data=None):
        """Analyze lab values for critical alerts"""
        alerts = []
        severity_counts = {'critical': 0, 'severe': 0, 'moderate': 0}
        
        for lab, value in lab_data.items():
            if lab in self.critical_thresholds:
                alert = self._check_single_value(lab, value, patient_data)
                if alert:
                    alerts.append(alert)
                    severity_counts[alert['severity']] += 1
        
        return {
            'alerts': alerts,
            'total_alerts': len(alerts),
            'severity_breakdown': severity_counts,
            'overall_risk': self._calculate_overall_risk(severity_counts),
            'immediate_actions': self._get_immediate_actions(alerts)
        }
    
    def analyze_trends(self, historical_data, timepoints=None):
        """Analyze trends in lab values over time"""
        trend_alerts = []
        
        for lab, values in historical_data.items():
            if len(values) >= 3:  # Need at least 3 points for trend analysis
                trend_analysis = self._analyze_single_trend(lab, values, timepoints)
                if trend_analysis['alert_level'] != 'none':
                    trend_alerts.append(trend_analysis)
        
        return {
            'trend_alerts': trend_alerts,
            'declining_parameters': [alert for alert in trend_alerts if alert['direction'] == 'declining'],
            'improving_parameters': [alert for alert in trend_alerts if alert['direction'] == 'improving'],
            'unstable_parameters': [alert for alert in trend_alerts if alert['direction'] == 'unstable'],
            'recommendations': self._get_trend_recommendations(trend_alerts)
        }
    
    def generate_smart_alerts(self, current_labs, historical_data=None, patient_data=None):
        """Generate comprehensive smart alerts combining current values and trends"""
        # Analyze current critical values
        critical_analysis = self.analyze_critical_values(current_labs, patient_data)
        
        # Analyze trends if historical data available
        trend_analysis = {}
        if historical_data:
            trend_analysis = self.analyze_trends(historical_data)
        
        # Generate contextual recommendations
        contextual_alerts = self._generate_contextual_alerts(current_labs, patient_data)
        
        # Prioritize alerts
        all_alerts = critical_analysis['alerts'] + trend_analysis.get('trend_alerts', []) + contextual_alerts
        prioritized_alerts = self._prioritize_alerts(all_alerts)
        
        return {
            'critical_values': critical_analysis,
            'trends': trend_analysis,
            'contextual_alerts': contextual_alerts,
            'prioritized_alerts': prioritized_alerts,
            'summary': self._generate_alert_summary(critical_analysis, trend_analysis, contextual_alerts),
            'next_monitoring': self._recommend_monitoring_schedule(all_alerts, patient_data)
        }
    
    def _check_single_value(self, lab, value, patient_data=None):
        """Check a single lab value against thresholds"""
        thresholds = self.critical_thresholds[lab]
        
        # Handle bidirectional parameters (potassium, calcium)
        if 'critical_high' in thresholds:
            if value >= thresholds['critical_high'] or value <= thresholds['critical_low']:
                severity = 'critical'
                direction = 'high' if value >= thresholds['critical_high'] else 'low'
            elif value >= thresholds['severe_high'] or value <= thresholds['severe_low']:
                severity = 'severe'
                direction = 'high' if value >= thresholds['severe_high'] else 'low'
            else:
                return None
        else:
            # Handle unidirectional parameters
            if 'critical' in thresholds:
                if (lab in ['creatinine', 'bun', 'phosphorus'] and value >= thresholds['critical']) or \
                   (lab in ['gfr', 'hemoglobin', 'albumin'] and value <= thresholds['critical']):
                    severity = 'critical'
                elif (lab in ['creatinine', 'bun', 'phosphorus'] and value >= thresholds['severe']) or \
                     (lab in ['gfr', 'hemoglobin', 'albumin'] and value <= thresholds['severe']):
                    severity = 'severe'
                elif (lab in ['creatinine', 'bun', 'phosphorus'] and value >= thresholds['moderate']) or \
                     (lab in ['gfr', 'hemoglobin', 'albumin'] and value <= thresholds['moderate']):
                    severity = 'moderate'
                else:
                    return None
                direction = 'high' if lab in ['creatinine', 'bun', 'phosphorus'] else 'low'
        
        return {
            'lab': lab,
            'value': value,
            'severity': severity,
            'direction': direction,
            'message': self._generate_alert_message(lab, value, severity, direction),
            'actions': self._get_recommended_actions(lab, severity, patient_data),
            'urgency': self._calculate_urgency(severity, lab, patient_data)
        }
    
    def _analyze_single_trend(self, lab, values, timepoints=None):
        """Analyze trend for a single parameter"""
        if len(values) < 3:
            return {'alert_level': 'none'}
        
        # Calculate trend metrics
        recent_change = (values[-1] - values[-2]) / values[-2] if values[-2] != 0 else 0
        overall_change = (values[-1] - values[0]) / values[0] if values[0] != 0 else 0
        
        # Determine trend direction and severity
        if abs(overall_change) >= self.trend_thresholds['rapid_decline']:
            alert_level = 'critical'
        elif abs(overall_change) >= self.trend_thresholds['concerning_trend']:
            alert_level = 'moderate'
        elif abs(recent_change) >= self.trend_thresholds['concerning_trend']:
            alert_level = 'mild'
        else:
            alert_level = 'none'
        
        direction = 'declining' if overall_change < -0.1 else 'improving' if overall_change > 0.1 else 'stable'
        
        return {
            'lab': lab,
            'alert_level': alert_level,
            'direction': direction,
            'recent_change_percent': recent_change * 100,
            'overall_change_percent': overall_change * 100,
            'values': values,
            'message': f"{lab.title()} showing {direction} trend ({overall_change*100:.1f}% change)",
            'recommendation': self._get_trend_recommendation(lab, direction, alert_level)
        }
    
    def _generate_contextual_alerts(self, current_labs, patient_data=None):
        """Generate contextual alerts based on patient-specific factors"""
        alerts = []
        
        if patient_data:
            # Diabetes-specific alerts
            if patient_data.get('diabetes') and current_labs.get('creatinine', 0) > 1.5:
                alerts.append({
                    'type': 'contextual',
                    'category': 'diabetic_nephropathy',
                    'severity': 'moderate',
                    'message': 'Elevated creatinine in diabetic patient - monitor for diabetic nephropathy progression',
                    'actions': ['Consider ACE inhibitor/ARB', 'Optimize glycemic control', 'Monitor proteinuria']
                })
            
            # Age-specific alerts
            if patient_data.get('age', 0) > 75 and current_labs.get('gfr', 100) < 45:
                alerts.append({
                    'type': 'contextual',
                    'category': 'elderly_ckd',
                    'severity': 'moderate',
                    'message': 'Elderly patient with moderate CKD - increased risk for complications',
                    'actions': ['Review medications for dose adjustments', 'Monitor for CKD-MBD', 'Consider nephrology referral']
                })
        
        return alerts
    
    def _calculate_overall_risk(self, severity_counts):
        """Calculate overall risk level"""
        if severity_counts['critical'] > 0:
            return 'critical'
        elif severity_counts['severe'] > 1:
            return 'high'
        elif severity_counts['severe'] > 0 or severity_counts['moderate'] > 2:
            return 'moderate'
        else:
            return 'low'
    
    def _get_immediate_actions(self, alerts):
        """Get immediate actions based on alerts"""
        actions = []
        critical_alerts = [alert for alert in alerts if alert['severity'] == 'critical']
        
        if critical_alerts:
            actions.append('Immediate physician notification required')
            actions.append('Consider emergency department evaluation')
            actions.append('Hold nephrotoxic medications')
        
        return actions
    
    def _generate_alert_message(self, lab, value, severity, direction):
        """Generate human-readable alert message"""
        severity_text = {'critical': 'CRITICAL', 'severe': 'SEVERE', 'moderate': 'MODERATE'}[severity]
        direction_text = {'high': 'elevated', 'low': 'low'}[direction]
        
        return f"{severity_text}: {lab.title()} is {direction_text} at {value} - immediate attention required"
    
    def _get_recommended_actions(self, lab, severity, patient_data=None):
        """Get recommended actions for specific lab abnormalities"""
        actions = []
        
        if lab == 'creatinine' and severity in ['critical', 'severe']:
            actions.extend(['Nephrology consultation', 'Review medications', 'Check for obstruction'])
        elif lab == 'potassium' and severity == 'critical':
            actions.extend(['ECG monitoring', 'Consider dialysis', 'Calcium gluconate if needed'])
        elif lab == 'hemoglobin' and severity in ['critical', 'severe']:
            actions.extend(['Iron studies', 'Consider ESA therapy', 'Rule out bleeding'])
        
        return actions
    
    def _calculate_urgency(self, severity, lab, patient_data=None):
        """Calculate urgency level"""
        if severity == 'critical':
            return 'immediate'
        elif severity == 'severe':
            return 'within_4_hours'
        else:
            return 'within_24_hours'
    
    def _prioritize_alerts(self, alerts):
        """Prioritize alerts by severity and urgency"""
        priority_order = {'critical': 3, 'severe': 2, 'moderate': 1, 'mild': 0}
        return sorted(alerts, key=lambda x: priority_order.get(x.get('severity', 'mild'), 0), reverse=True)
    
    def _generate_alert_summary(self, critical_analysis, trend_analysis, contextual_alerts):
        """Generate summary of all alerts"""
        total_alerts = critical_analysis['total_alerts'] + len(trend_analysis.get('trend_alerts', [])) + len(contextual_alerts)
        
        if total_alerts == 0:
            return "No critical alerts detected. Continue routine monitoring."
        
        summary = f"Total of {total_alerts} alerts detected. "
        if critical_analysis['severity_breakdown']['critical'] > 0:
            summary += f"CRITICAL: {critical_analysis['severity_breakdown']['critical']} critical values require immediate attention. "
        
        return summary
    
    def _recommend_monitoring_schedule(self, alerts, patient_data=None):
        """Recommend monitoring schedule based on alerts"""
        if any(alert.get('severity') == 'critical' for alert in alerts):
            return {'frequency': 'daily', 'duration': '1 week', 'parameters': 'all critical values'}
        elif any(alert.get('severity') == 'severe' for alert in alerts):
            return {'frequency': 'every 2-3 days', 'duration': '2 weeks', 'parameters': 'affected parameters'}
        else:
            return {'frequency': 'weekly', 'duration': '1 month', 'parameters': 'routine monitoring'}
    
    def _get_trend_recommendation(self, lab, direction, alert_level):
        """Get recommendation for trend analysis"""
        if direction == 'declining' and alert_level in ['critical', 'moderate']:
            return f"Urgent evaluation needed for declining {lab} - consider intervention"
        elif direction == 'improving':
            return f"{lab.title()} showing improvement - continue current management"
        else:
            return f"Monitor {lab} closely for continued changes"
    
    def _get_trend_recommendations(self, trend_alerts):
        """Get overall trend recommendations"""
        recommendations = []
        
        declining_count = len([alert for alert in trend_alerts if alert['direction'] == 'declining'])
        if declining_count > 0:
            recommendations.append(f"Urgent attention: {declining_count} parameters showing concerning decline")
        
        return recommendations


class MLOutcomePrediction:
    """Machine Learning-based patient outcome prediction models"""
    
    def __init__(self):
        self.models_initialized = True
        
    def predict_dialysis_initiation(self, patient_data, lab_data, historical_data=None):
        """Predict likelihood and timeline for dialysis initiation"""
        try:
            # Extract key features for dialysis prediction
            gfr = lab_data.get('gfr', 30)
            creatinine = lab_data.get('creatinine', 3.0)
            age = patient_data.get('age', 65)
            diabetes = patient_data.get('diabetes', False)
            hypertension = patient_data.get('hypertension', False)
            
            # Calculate risk score based on clinical guidelines and ML patterns
            risk_score = 0
            
            # GFR-based scoring (primary factor)
            if gfr <= 10:
                risk_score += 40
                timeline = "1-3 months"
            elif gfr <= 15:
                risk_score += 30
                timeline = "3-6 months"
            elif gfr <= 20:
                risk_score += 20
                timeline = "6-12 months"
            else:
                risk_score += 10
                timeline = "12+ months"
            
            # Creatinine adjustment
            if creatinine >= 5.0:
                risk_score += 15
            elif creatinine >= 4.0:
                risk_score += 10
            
            # Comorbidity factors
            if diabetes:
                risk_score += 15
            if hypertension:
                risk_score += 10
            
            # Age factor
            if age >= 75:
                risk_score += 10
            elif age >= 65:
                risk_score += 5
            
            # Historical trend analysis
            if historical_data:
                gfr_trend = historical_data.get('gfr', [])
                if len(gfr_trend) >= 3:
                    recent_decline = (gfr_trend[0] - gfr_trend[-1]) / len(gfr_trend)
                    if recent_decline > 5:  # Rapid decline
                        risk_score += 15
                        timeline = self._adjust_timeline_for_decline(timeline, recent_decline)
            
            # Calculate probability
            probability = min(risk_score / 100.0, 0.95)
            
            # Determine risk level
            if probability >= 0.7:
                risk_level = "high"
            elif probability >= 0.4:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            return {
                'probability': probability,
                'risk_level': risk_level,
                'timeline': timeline,
                'risk_score': risk_score,
                'key_factors': self._get_dialysis_risk_factors(patient_data, lab_data),
                'recommendations': self._get_dialysis_preparation_recommendations(risk_level, timeline)
            }
            
        except Exception as e:
            return {'error': f"Dialysis prediction failed: {str(e)}"}
    
    def predict_transplant_success(self, patient_data, lab_data, donor_data=None):
        """Predict transplant success probability and outcomes"""
        try:
            age = patient_data.get('age', 65)
            diabetes = patient_data.get('diabetes', False)
            cardiovascular_disease = patient_data.get('cardiovascular_disease', False)
            gfr = lab_data.get('gfr', 15)
            albumin = lab_data.get('albumin', 3.5)
            hemoglobin = lab_data.get('hemoglobin', 10.0)
            
            # Base success score
            success_score = 70  # Start with 70% base success rate
            
            # Age factor
            if age <= 50:
                success_score += 15
            elif age <= 65:
                success_score += 5
            elif age >= 75:
                success_score -= 15
            
            # Comorbidity factors
            if diabetes:
                success_score -= 10
            if cardiovascular_disease:
                success_score -= 15
            
            # Lab factors
            if albumin >= 3.5:
                success_score += 10
            elif albumin < 2.5:
                success_score -= 15
            
            if hemoglobin >= 11.0:
                success_score += 5
            elif hemoglobin < 9.0:
                success_score -= 10
            
            # Donor factors (if available)
            if donor_data:
                donor_age = donor_data.get('age', 45)
                donor_type = donor_data.get('type', 'deceased')  # living or deceased
                
                if donor_type == 'living':
                    success_score += 20
                
                if donor_age <= 35:
                    success_score += 10
                elif donor_age >= 60:
                    success_score -= 10
            
            # Normalize to probability
            probability = min(max(success_score / 100.0, 0.1), 0.95)
            
            # Risk stratification
            if probability >= 0.8:
                risk_category = "excellent"
            elif probability >= 0.65:
                risk_category = "good"
            elif probability >= 0.5:
                risk_category = "moderate"
            else:
                risk_category = "high_risk"
            
            return {
                'success_probability': probability,
                'risk_category': risk_category,
                'five_year_survival': probability * 0.9,  # Approximate 5-year survival
                'ten_year_survival': probability * 0.75,  # Approximate 10-year survival
                'key_factors': self._get_transplant_factors(patient_data, lab_data, donor_data),
                'optimization_recommendations': self._get_transplant_optimization_recommendations(risk_category)
            }
            
        except Exception as e:
            return {'error': f"Transplant prediction failed: {str(e)}"}
    
    def predict_mortality_risk(self, patient_data, lab_data, historical_data=None):
        """Predict mortality risk using validated CKD risk models"""
        try:
            age = patient_data.get('age', 65)
            gender = patient_data.get('gender', 'male')
            diabetes = patient_data.get('diabetes', False)
            cardiovascular_disease = patient_data.get('cardiovascular_disease', False)
            
            gfr = lab_data.get('gfr', 30)
            albumin = lab_data.get('albumin', 3.5)
            hemoglobin = lab_data.get('hemoglobin', 10.0)
            phosphorus = lab_data.get('phosphorus', 4.5)
            
            # Base mortality risk calculation (adapted from validated models)
            risk_score = 0
            
            # Age factor (strongest predictor)
            if age >= 80:
                risk_score += 30
            elif age >= 70:
                risk_score += 20
            elif age >= 60:
                risk_score += 10
            
            # Gender factor
            if gender.lower() == 'male':
                risk_score += 5
            
            # GFR factor
            if gfr < 15:
                risk_score += 25
            elif gfr < 30:
                risk_score += 15
            elif gfr < 45:
                risk_score += 8
            
            # Comorbidity factors
            if diabetes:
                risk_score += 15
            if cardiovascular_disease:
                risk_score += 20
            
            # Lab factors
            if albumin < 3.0:
                risk_score += 15
            elif albumin < 3.5:
                risk_score += 8
            
            if hemoglobin < 9.0:
                risk_score += 10
            elif hemoglobin < 10.0:
                risk_score += 5
            
            if phosphorus > 5.5:
                risk_score += 8
            
            # Convert to probability (1-year mortality risk)
            one_year_risk = min(risk_score / 200.0, 0.5)  # Cap at 50%
            five_year_risk = min(one_year_risk * 3.5, 0.8)  # Approximate 5-year risk
            
            # Risk stratification
            if one_year_risk >= 0.2:
                risk_level = "very_high"
            elif one_year_risk >= 0.1:
                risk_level = "high"
            elif one_year_risk >= 0.05:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            return {
                'one_year_mortality_risk': one_year_risk,
                'five_year_mortality_risk': five_year_risk,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'primary_risk_factors': self._get_mortality_risk_factors(patient_data, lab_data),
                'interventions': self._get_mortality_reduction_interventions(risk_level)
            }
            
        except Exception as e:
            return {'error': f"Mortality prediction failed: {str(e)}"}
    
    def predict_disease_progression(self, patient_data, lab_data, historical_data=None):
        """Predict CKD progression rate and future GFR"""
        try:
            current_gfr = lab_data.get('gfr', 30)
            age = patient_data.get('age', 65)
            diabetes = patient_data.get('diabetes', False)
            hypertension = patient_data.get('hypertension', False)
            proteinuria = lab_data.get('proteinuria', 'moderate')
            
            # Base progression rate (mL/min/1.73m²/year)
            base_decline = 2.0  # Normal aging
            
            # Disease-specific factors
            if diabetes:
                base_decline += 3.0
            if hypertension:
                base_decline += 2.0
            
            # Proteinuria factor
            if proteinuria == 'severe' or lab_data.get('protein_creatinine_ratio', 1.0) > 3.0:
                base_decline += 4.0
            elif proteinuria == 'moderate' or lab_data.get('protein_creatinine_ratio', 1.0) > 1.0:
                base_decline += 2.0
            
            # Age factor
            if age >= 70:
                base_decline += 1.0
            
            # Historical trend analysis
            if historical_data and 'gfr' in historical_data:
                gfr_history = historical_data['gfr']
                if len(gfr_history) >= 3:
                    # Calculate actual decline rate
                    time_span = len(gfr_history) - 1  # Assuming monthly measurements
                    actual_decline = (gfr_history[0] - gfr_history[-1]) / (time_span / 12.0)  # Per year
                    
                    # Use actual rate if available, weighted with predicted
                    base_decline = (base_decline + actual_decline * 2) / 3
            
            # Project future GFR
            projections = {}
            for years in [1, 2, 3, 5]:
                projected_gfr = max(current_gfr - (base_decline * years), 5)
                projections[f'{years}_year'] = projected_gfr
            
            # Determine progression rate category
            if base_decline >= 5.0:
                progression_rate = "rapid"
            elif base_decline >= 3.0:
                progression_rate = "moderate"
            else:
                progression_rate = "slow"
            
            # Estimate time to ESRD (GFR < 15)
            if base_decline > 0:
                years_to_esrd = max((current_gfr - 15) / base_decline, 0)
                if years_to_esrd > 20:
                    years_to_esrd = None  # May not reach ESRD
            else:
                years_to_esrd = None
            
            return {
                'annual_decline_rate': base_decline,
                'progression_rate': progression_rate,
                'gfr_projections': projections,
                'years_to_esrd': years_to_esrd,
                'key_factors': self._get_progression_factors(patient_data, lab_data),
                'interventions': self._get_progression_interventions(progression_rate)
            }
            
        except Exception as e:
            return {'error': f"Progression prediction failed: {str(e)}"}
    
    def _adjust_timeline_for_decline(self, timeline, decline_rate):
        """Adjust dialysis timeline based on GFR decline rate"""
        if decline_rate > 10:  # Very rapid decline
            timeline_map = {
                "12+ months": "6-9 months",
                "6-12 months": "3-6 months",
                "3-6 months": "1-3 months",
                "1-3 months": "Immediate"
            }
            return timeline_map.get(timeline, timeline)
        return timeline
    
    def _get_dialysis_risk_factors(self, patient_data, lab_data):
        """Get key risk factors for dialysis initiation"""
        factors = []
        if lab_data.get('gfr', 30) <= 15:
            factors.append("Severely reduced GFR")
        if lab_data.get('creatinine', 3.0) >= 4.0:
            factors.append("Elevated creatinine")
        if patient_data.get('diabetes', False):
            factors.append("Diabetes mellitus")
        if patient_data.get('hypertension', False):
            factors.append("Hypertension")
        return factors
    
    def _get_dialysis_preparation_recommendations(self, risk_level, timeline):
        """Get dialysis preparation recommendations"""
        if risk_level == "high":
            return [
                "Urgent nephrology consultation",
                "Vascular access planning (fistula creation)",
                "Pre-dialysis education",
                "Transplant evaluation if eligible",
                "Optimize cardiovascular health"
            ]
        elif risk_level == "moderate":
            return [
                "Regular nephrology follow-up",
                "Consider vascular access planning",
                "Patient education on RRT options",
                "Optimize blood pressure and diabetes control"
            ]
        else:
            return [
                "Continue CKD management",
                "Monitor progression closely",
                "Lifestyle modifications"
            ]
    
    def _get_transplant_factors(self, patient_data, lab_data, donor_data):
        """Get key factors affecting transplant success"""
        factors = []
        if patient_data.get('age', 65) <= 50:
            factors.append("Favorable age")
        if not patient_data.get('diabetes', False):
            factors.append("No diabetes")
        if lab_data.get('albumin', 3.5) >= 3.5:
            factors.append("Good nutritional status")
        if donor_data and donor_data.get('type') == 'living':
            factors.append("Living donor")
        return factors
    
    def _get_transplant_optimization_recommendations(self, risk_category):
        """Get transplant optimization recommendations"""
        base_recs = [
            "Maintain optimal nutrition",
            "Regular exercise as tolerated",
            "Vaccination updates",
            "Dental care optimization"
        ]
        
        if risk_category in ["moderate", "high_risk"]:
            base_recs.extend([
                "Cardiovascular risk optimization",
                "Diabetes control improvement",
                "Weight management if needed"
            ])
        
        return base_recs
    
    def _get_mortality_risk_factors(self, patient_data, lab_data):
        """Get primary mortality risk factors"""
        factors = []
        if patient_data.get('age', 65) >= 70:
            factors.append("Advanced age")
        if patient_data.get('cardiovascular_disease', False):
            factors.append("Cardiovascular disease")
        if lab_data.get('albumin', 3.5) < 3.0:
            factors.append("Malnutrition")
        if lab_data.get('gfr', 30) < 15:
            factors.append("Advanced CKD")
        return factors
    
    def _get_mortality_reduction_interventions(self, risk_level):
        """Get interventions to reduce mortality risk"""
        if risk_level == "very_high":
            return [
                "Intensive medical management",
                "Palliative care consultation",
                "Advanced care planning",
                "Frequent monitoring"
            ]
        elif risk_level == "high":
            return [
                "Aggressive risk factor modification",
                "Cardiovascular protection",
                "Nutritional support",
                "Regular monitoring"
            ]
        else:
            return [
                "Standard CKD care",
                "Lifestyle modifications",
                "Regular follow-up"
            ]
    
    def _get_progression_factors(self, patient_data, lab_data):
        """Get key factors affecting disease progression"""
        factors = []
        if patient_data.get('diabetes', False):
            factors.append("Diabetes mellitus")
        if patient_data.get('hypertension', False):
            factors.append("Hypertension")
        if lab_data.get('proteinuria') == 'severe':
            factors.append("Severe proteinuria")
        return factors
    
    def _get_progression_interventions(self, progression_rate):
        """Get interventions to slow progression"""
        if progression_rate == "rapid":
            return [
                "Urgent nephrology referral",
                "Aggressive BP control (<130/80)",
                "ACE inhibitor/ARB optimization",
                "Strict diabetes control",
                "Protein restriction"
            ]
        elif progression_rate == "moderate":
            return [
                "Regular nephrology follow-up",
                "BP control (<140/90)",
                "RAAS blockade",
                "Diabetes management"
            ]
        else:
            return [
                "Standard CKD care",
                "Lifestyle modifications",
                "Monitor progression"
            ]


class AIClinicaIntelligence:
    """Main AI Clinical Intelligence coordinator"""
    
    def __init__(self):
        self.kidney_predictor = KidneyFunctionPredictor()
        self.decision_support = ClinicalDecisionSupport()
        self.alert_system = IntelligentAlerts()
        self.dialysis_predictor = DialysisReadinessPredictor()
        self.transplant_analyzer = TransplantReadinessAnalyzer()
        self.drug_dosing = DrugDosingRecommendations()
        self.clinical_nlp = ClinicalNotesNLP()
        self.intelligent_alerts = IntelligentAlerts()
        self.ml_predictions = MLOutcomePrediction()
    
    def comprehensive_analysis(self, patient_data, lab_data=None, medications=None, historical_data=None):
        """Perform comprehensive AI-powered clinical analysis"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'patient_id': patient_data.get('patient_id', 'unknown')
        }
        
        # Kidney function prediction
        gfr_prediction = self.kidney_predictor.predict_gfr(patient_data)
        progression_risk = self.kidney_predictor.predict_progression_risk(patient_data)
        
        results['predictions'] = {
            'gfr': gfr_prediction,
            'progression': progression_risk
        }
        
        # Clinical decision support
        treatment_recommendations = self.decision_support.get_treatment_recommendations(
            patient_data, gfr_prediction
        )
        results['recommendations'] = treatment_recommendations
        
        # Drug dosing recommendations
        if medications:
            drug_recommendations = self.decision_support.get_drug_dosing_recommendations(
                patient_data, medications
            )
            results['drug_dosing'] = drug_recommendations
        
        # Intelligent alerts
        if lab_data:
            critical_alerts = self.alert_system.check_critical_values(lab_data)
            results['critical_alerts'] = critical_alerts
        
        if historical_data:
            trend_alerts = self.alert_system.analyze_trends(historical_data)
            results['trend_alerts'] = trend_alerts
        
        # Add dialysis and transplant readiness analysis
        dialysis_analysis = self.dialysis_predictor.predict_dialysis_timing(
            patient_data, lab_data, patient_data.get('symptoms', [])
        )
        results['dialysis_readiness'] = dialysis_analysis
        
        transplant_analysis = self.transplant_analyzer.analyze_transplant_eligibility(
            patient_data, lab_data, patient_data.get('comorbidities', [])
        )
        results['transplant_readiness'] = transplant_analysis
        
        return results
    
    def get_dialysis_readiness_assessment(self, patient_data):
        """Assess patient readiness for dialysis"""
        current_gfr = patient_data.get('current_gfr', 60)
        symptoms = patient_data.get('uremic_symptoms', [])
        
        readiness_score = 0
        factors = []
        
        # GFR-based assessment
        if current_gfr < 15:
            readiness_score += 40
            factors.append('GFR <15 mL/min/1.73m²')
        elif current_gfr < 20:
            readiness_score += 20
            factors.append('GFR <20 mL/min/1.73m²')
        
        # Symptom-based assessment
        uremic_symptoms = ['nausea', 'vomiting', 'fatigue', 'shortness_of_breath', 'confusion']
        symptom_count = sum(1 for symptom in uremic_symptoms if symptom in symptoms)
        readiness_score += symptom_count * 10
        
        if symptom_count > 0:
            factors.append(f'{symptom_count} uremic symptoms present')
        
        # Fluid overload
        if patient_data.get('fluid_overload'):
            readiness_score += 15
            factors.append('Fluid overload')
        
        # Electrolyte imbalances
        if patient_data.get('hyperkalemia'):
            readiness_score += 15
            factors.append('Hyperkalemia')
        
        # Metabolic acidosis
        if patient_data.get('metabolic_acidosis'):
            readiness_score += 10
            factors.append('Metabolic acidosis')
        
        # Determine readiness level
        if readiness_score >= 60:
            readiness = 'Immediate'
        elif readiness_score >= 40:
            readiness = 'Within 3-6 months'
        elif readiness_score >= 20:
            readiness = 'Within 6-12 months'
        else:
            readiness = 'Not yet indicated'
        
        return {
            'readiness_level': readiness,
            'readiness_score': readiness_score,
            'contributing_factors': factors,
            'recommendations': self._get_dialysis_preparation_recommendations(readiness_score)
        }
    
    def _get_dialysis_preparation_recommendations(self, score):
        """Get dialysis preparation recommendations based on readiness score"""
        recommendations = []
        
        if score >= 40:
            recommendations.extend([
                'Urgent nephrology consultation',
                'Vascular access planning and creation',
                'Patient education on dialysis modalities',
                'Nutritionist consultation',
                'Social work evaluation'
            ])
        elif score >= 20:
            recommendations.extend([
                'Nephrology follow-up within 1-3 months',
                'Begin vascular access planning',
                'Patient education on CKD progression',
                'Optimize medical management'
            ])
        else:
            recommendations.extend([
                'Continue conservative management',
                'Regular nephrology follow-up',
                'Monitor for progression'
            ])
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    # Initialize AI Clinical Intelligence
    ai_clinical = AIClinicaIntelligence()
    
    # Example patient data
    sample_patient = {
        'patient_id': 'P001',
        'age': 65,
        'gender': 'male',
        'bmi': 28.5,
        'current_gfr': 35,
        'creatinine': 2.1,
        'bun': 45,
        'albumin': 3.2,
        'hemoglobin': 9.8,
        'phosphorus': 4.2,
        'calcium': 8.9,
        'pth': 125,
        'diabetes': True,
        'hypertension': True,
        'cardiovascular_disease': False,
        'proteinuria': True,
        'ace_inhibitor': True,
        'arb': False,
        'diuretic': True
    }
    
    # Example lab data
    sample_labs = {
        'creatinine': 2.1,
        'potassium': 5.2,
        'hemoglobin': 9.8,
        'calcium': 8.9
    }
    
    # Example medications
    sample_medications = ['metformin', 'lisinopril', 'furosemide']
    
    # Perform comprehensive analysis
    analysis = ai_clinical.comprehensive_analysis(
        sample_patient, 
        sample_labs, 
        sample_medications
    )
    
    print("AI Clinical Intelligence Analysis:")
    print("=" * 50)
    print(f"Patient ID: {analysis['patient_id']}")
    print(f"Analysis Time: {analysis['timestamp']}")
    print("\nPredictions:")
    print(f"  Predicted GFR: {analysis['predictions']['gfr']['predicted_gfr']} mL/min/1.73m²")
    print(f"  CKD Stage: {analysis['predictions']['gfr']['stage']}")
    print(f"  Progression Risk: {analysis['predictions']['progression']['risk_level']} ({analysis['predictions']['progression']['progression_risk']}%)")
    
    print("\nTreatment Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  • {rec['category']}: {rec['recommendation']}")
    
    if 'critical_alerts' in analysis and analysis['critical_alerts']:
        print("\nCritical Alerts:")
        for alert in analysis['critical_alerts']:
            print(f"  ⚠️ {alert['type']}: {alert['lab']} = {alert['value']} ({alert['urgency']})")
    
    # Dialysis readiness assessment
    dialysis_assessment = ai_clinical.get_dialysis_readiness_assessment(sample_patient)
    print(f"\nDialysis Readiness: {dialysis_assessment['readiness_level']}")
    print(f"Readiness Score: {dialysis_assessment['readiness_score']}/100")