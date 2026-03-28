import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_report_with_ai(report_text: str):
    prompt = """
    You are an expert AI clinical data extractor and interpreter. 
    Analyze the following medical report text and extract the individual test results, and then provide a short list of probable differential diagnoses (maximum 3) based ONLY on the abnormal values found.
    
    Return the output EXCLUSIVELY as a JSON object with two keys: "results" and "diagnoses". Do not include markdown formatting like ```json.
    
    Example output format:
    {
      "results": [
        {
            "test_name": "Hemoglobin",
            "value": "9.2 g/dL",
            "reference_range": "12.0-16.0 g/dL",
            "status": "Low",
            "explanation": "Your hemoglobin is low, which may indicate anemia."
        }
      ],
      "diagnoses": [
        {
            "name": "Iron Deficiency Anemia",
            "sub": "Suggested by low Hemoglobin",
            "prob": 80
        }
      ]
    }

    Medical Report Text:
    {report_text}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt.replace("{report_text}", report_text)
                }
            ],
            model=GROQ_MODEL,
            temperature=0.1, # Low temperature for more deterministic extraction
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Clean up response if the model returned markdown code blocks
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
        if response_text.endswith("```"):
            response_text = response_text.rsplit("```", 1)[0]
            
        return json.loads(response_text.strip())
        
    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        # Fallback to empty list or raise
        raise Exception("Failed to analyze report with AI.")


def generate_treatment_plan(analysis_results: dict):
    """
    Generate a treatment/management plan based on previously analyzed report data.
    Takes the full analysis output (results + diagnoses) and produces lifestyle,
    medication guidance, doctor referrals, and risk stratification.
    """
    
    # Build a summary of findings to send to AI
    results_summary = json.dumps(analysis_results, indent=2)
    
    prompt = f"""
You are an expert AI clinical advisor providing EDUCATIONAL health guidance.
Based on the following medical report analysis, generate a comprehensive management plan.

CRITICAL SAFETY RULES:
- Do NOT provide exact prescriptions or final drug orders
- Do NOT replace a doctor — always recommend consulting one
- Only suggest GENERAL medication classes, not specific dosages
- Always include the disclaimer: "This is not a medical prescription. Consult a licensed doctor before taking any medication."

Analysis Data:
{results_summary}

Return the output EXCLUSIVELY as a JSON object with these keys. Do not include markdown formatting like ```json.

{{
  "condition_overview": "A 2-3 sentence summary of the overall clinical picture based on the abnormal findings",
  "lifestyle_changes": [
    "Specific diet recommendation",
    "Exercise recommendation", 
    "Sleep/stress recommendation"
  ],
  "treatment_options": [
    "General treatment approach 1",
    "General treatment approach 2"
  ],
  "medications": [
    "General medication class 1 (e.g., iron supplements)",
    "General medication class 2 (e.g., vitamin B12)"
  ],
  "doctor_recommendation": [
    "Specialist type 1 (e.g., Hematologist)",
    "Specialist type 2 (e.g., General Physician)"
  ],
  "monitoring_advice": [
    "Follow-up test recommendation 1",
    "Follow-up test recommendation 2"
  ],
  "risk_level": "Mild OR Moderate OR Severe",
  "disclaimer": "This is not a medical prescription. Consult a licensed doctor before taking any medication."
}}

Provide at least 3 lifestyle changes, 2 treatment options, 2 medication classes, 2 doctor recommendations, and 2 monitoring items.
Be specific and personalized to the actual findings — do not give generic advice.
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=GROQ_MODEL,
            temperature=0.3,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Clean up response if the model returned markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json", 1)[1]
        if "```" in response_text:
            response_text = response_text.split("```", 1)[0]
            
        return json.loads(response_text.strip())
        
    except Exception as e:
        print(f"Error generating treatment plan: {str(e)}")
        # Return a fallback plan so the main analysis still works
        return {
            "condition_overview": "Unable to generate a detailed management plan at this time. Please consult your healthcare provider.",
            "lifestyle_changes": ["Maintain a balanced diet", "Engage in regular moderate exercise", "Ensure adequate sleep (7-8 hours)"],
            "treatment_options": ["Consult your healthcare provider for personalized treatment"],
            "medications": ["Consult your doctor for appropriate medication guidance"],
            "doctor_recommendation": ["General Physician"],
            "monitoring_advice": ["Schedule a follow-up appointment with your doctor"],
            "risk_level": "Moderate",
            "disclaimer": "This is not a medical prescription. Consult a licensed doctor before taking any medication."
        }
