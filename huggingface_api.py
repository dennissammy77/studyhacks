import requests

API_URL = "https://api-inference.huggingface.co/models/pszemraj/led-large-book-summary"

def query(payload, SECRET_KEY):
    headers = {"Authorization": f"Bearer {SECRET_KEY}"}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Hugging Face API request failed"}, response.status_code
