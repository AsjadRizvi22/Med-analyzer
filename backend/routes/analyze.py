from fastapi import APIRouter, HTTPException
from models.schemas import AnalyzerRequest, AnalyzerResponse, TestResult, TreatmentPlan
from services.ai_service import analyze_report_with_ai, generate_treatment_plan
from services.db_service import save_report_and_results, save_treatment_plan

router = APIRouter()

@router.post("/analyze", response_model=AnalyzerResponse)
async def analyze_report(request: AnalyzerRequest):
    if not request.report_text or not request.report_text.strip():
        raise HTTPException(status_code=400, detail="Report text cannot be empty")
        
    try:
        # 1. Analyze text using AI (returns a dict now)
        extracted_data = analyze_report_with_ai(request.report_text)
        
        raw_results = extracted_data.get("results", [])
        raw_diagnoses = extracted_data.get("diagnoses", [])
        
        # 2. Convert to Pydantic models
        test_results = []
        for res in raw_results:
            test_results.append(TestResult(
                test_name=res.get("test_name", "Unknown"),
                value=str(res.get("value", "N/A")),
                reference_range=str(res.get("reference_range", "N/A")),
                status=res.get("status", "Unknown"),
                explanation=res.get("explanation", "")
            ))
            
        diagnoses = []
        for d in raw_diagnoses:
            diagnoses.append({
                "name": str(d.get("name", "Unknown")),
                "sub": str(d.get("sub", "")),
                "prob": int(d.get("prob", 50))
            })
        
        # 3. Generate Treatment Plan using AI
        raw_plan = generate_treatment_plan(extracted_data)
        treatment_plan = TreatmentPlan(
            condition_overview=raw_plan.get("condition_overview", ""),
            lifestyle_changes=raw_plan.get("lifestyle_changes", []),
            treatment_options=raw_plan.get("treatment_options", []),
            medications=raw_plan.get("medications", []),
            doctor_recommendation=raw_plan.get("doctor_recommendation", []),
            monitoring_advice=raw_plan.get("monitoring_advice", []),
            risk_level=raw_plan.get("risk_level", "Moderate"),
            disclaimer=raw_plan.get("disclaimer", "This is not a medical prescription. Consult a licensed doctor before taking any medication.")
        )
            
        # 4. Save to database (report + results, then treatment plan)
        report_id = save_report_and_results(request.user_id, request.report_text, raw_results)
        if report_id:
            save_treatment_plan(report_id, raw_plan)
        
        # 5. Return response
        return AnalyzerResponse(
            results=test_results,
            diagnoses=diagnoses,
            treatment_plan=treatment_plan
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
