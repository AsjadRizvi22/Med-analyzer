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
    Analyze the following medical report text and extract the individual test results.
    For each test result found, provide:
    1. test_name: Name of the test
    2. value: The patient's result value
    3. reference_range: The normal reference range (if provided or known)
    4. status: Must be exactly "Low", "Normal", or "High" based on the value and reference range.
    5. explanation: A simple, patient-friendly one-sentence explanation of what this test measures and what the result means.

    Return the output EXCLUSIVELY as a JSON array of objects. Do not include markdown formatting like ```json.
    Example output format:
    [
        {
            "test_name": "Hemoglobin",
            "value": "9.2 g/dL",
            "reference_range": "12.0-16.0 g/dL",
            "status": "Low",
            "explanation": "Your hemoglobin is low, which may indicate anemia."
        }
    ]

    Medical Report Text:
    {report_text}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(report_text=report_text)
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
