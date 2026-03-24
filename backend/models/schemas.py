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

class AnalyzerResponse(BaseModel):
    results: List[TestResult]
    diagnoses: List[Diagnosis] = []
    disclaimer: str = "Medical Disclaimer: This tool is for educational and informational purposes only. Results generated are not a medical diagnosis. Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment."
