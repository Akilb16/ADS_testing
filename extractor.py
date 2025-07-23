import requests

AI_BACKEND_URL = "https://ai-backend-vtzb.onrender.com/extract-invoice"

def extract_invoice(file):
    try:
        response = requests.post(
            AI_BACKEND_URL,
            files={"file": (file.name, file, file.type)}
        )
        print(response.json())
        if response.status_code == 200:
            
            return response.json().get("data", {})
    except Exception as e:
        print("AI Extraction error:", e)
    return None
