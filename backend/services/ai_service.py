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
