import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # using service role key as provided

def get_supabase_client() -> Client:
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

def save_report_and_results(user_id: str, report_text: str, results: list):
    db = get_supabase_client()
    if not db:
        print("Supabase not configured. Skipping DB save.")
        return None

    try:
        # 1. Save Report
        report_data = {
            "report_text": report_text
        }
        if user_id:
            report_data["user_id"] = user_id
            
        report_res = db.table("reports").insert(report_data).execute()
        report_id = report_res.data[0]["id"]
        
        # 2. Save Results
        for result in results:
            result_data = {
                "report_id": report_id,
                "test_name": result.get("test_name"),
                "value": str(result.get("value")),
                "reference_range": str(result.get("reference_range", "")),
                "status": result.get("status"),
                "explanation": result.get("explanation")
            }
            db.table("results").insert(result_data).execute()
        
        return report_id
            
    except Exception as e:
        print(f"Failed to save to Supabase: {str(e)}")
        # We catch exceptions so that the main API flow isn't interrupted if DB save fails
        # since DB tables might not be created yet.
        return None


def save_treatment_plan(report_id: str, treatment_plan: dict):
    """Save the treatment plan to the treatment_plans table in Supabase."""
    db = get_supabase_client()
    if not db or not report_id:
        print("Supabase not configured or no report_id. Skipping treatment plan save.")
        return

    try:
        plan_data = {
            "report_id": report_id,
            "condition_overview": treatment_plan.get("condition_overview", ""),
            "lifestyle": json.dumps(treatment_plan.get("lifestyle_changes", [])),
            "treatment": json.dumps(treatment_plan.get("treatment_options", [])),
            "medications": json.dumps(treatment_plan.get("medications", [])),
            "doctor_recommendation": json.dumps(treatment_plan.get("doctor_recommendation", [])),
            "risk_level": treatment_plan.get("risk_level", "Moderate"),
            "monitoring_advice": json.dumps(treatment_plan.get("monitoring_advice", []))
        }
        db.table("treatment_plans").insert(plan_data).execute()
        
    except Exception as e:
        print(f"Failed to save treatment plan to Supabase: {str(e)}")
        # Non-blocking — don't interrupt the API flow
