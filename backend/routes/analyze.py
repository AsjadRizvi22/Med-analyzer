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
        # 1. Analyze text using AI
        extracted_results = analyze_report_with_ai(request.report_text)
        
        # 2. Convert to Pydantic models
        test_results = []
        for res in extracted_results:
            test_results.append(TestResult(
                test_name=res.get("test_name", "Unknown"),
                value=str(res.get("value", "N/A")),
                reference_range=str(res.get("reference_range", "N/A")),
                status=res.get("status", "Unknown"),
                explanation=res.get("explanation", "")
            ))
            
        # 3. Save to database asynchronously or in background (doing it synchronously here for simplicity)
        save_report_and_results(request.user_id, request.report_text, extracted_results)
        
        # 4. Return response
        return AnalyzerResponse(results=test_results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
