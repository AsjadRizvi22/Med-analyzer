from fastapi import APIRouter, HTTPException
from models.schemas import AnalyzerRequest, AnalyzerResponse, TestResult
from services.ai_service import analyze_report_with_ai
from services.db_service import save_report_and_results

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
            
        # 3. Save to database synchronously (only sending results array)
        save_report_and_results(request.user_id, request.report_text, raw_results)
        
        # 4. Return response
        return AnalyzerResponse(results=test_results, diagnoses=diagnoses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
