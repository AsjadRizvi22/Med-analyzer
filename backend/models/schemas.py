from pydantic import BaseModel
from typing import List, Optional

class AnalyzerRequest(BaseModel):
    report_text: str
    user_id: Optional[str] = None

class TestResult(BaseModel):
    test_name: str
    value: str
    reference_range: str
    status: str
    explanation: str

class Diagnosis(BaseModel):
    name: str
    sub: str
    prob: int

class TreatmentPlan(BaseModel):
    condition_overview: str = ""
    lifestyle_changes: List[str] = []
    treatment_options: List[str] = []
    medications: List[str] = []
    doctor_recommendation: List[str] = []
    monitoring_advice: List[str] = []
    risk_level: str = "Mild"
    disclaimer: str = "This is not a medical prescription. Consult a licensed doctor before taking any medication."

class AnalyzerResponse(BaseModel):
    results: List[TestResult]
    diagnoses: List[Diagnosis] = []
    treatment_plan: Optional[TreatmentPlan] = None
    disclaimer: str = "Medical Disclaimer: This tool is for educational and informational purposes only. Results generated are not a medical diagnosis. Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment."
