import requests

def get_output(system, prompt):
    API_URL = "https://l4npxqyj15m9kzl5.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept" : "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    prompt = system + prompt

    output = query({
        "inputs": prompt,
        "parameters": {
            "top_k": 150,
            "top_p": 0.20347480208997282,
            "temperature": 0.5954630385670282,
            "max_new_tokens": 726
        }
    })
    response = output[0]['generated_text'][:]
    return response
    