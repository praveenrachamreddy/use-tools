import requests
import json
import os
from .base_model import BaseModel

class OpenAIModel(BaseModel):
    def __init__(self, model, system_prompt, temperature):
        super().__init__(model, system_prompt, temperature)
        self.model_endpoint = 'https://api.openai.com/v1/chat/completions'
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def generate_text(self, prompt):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "stream": False
        }
        
        response = requests.post(self.model_endpoint, headers=self.headers, data=json.dumps(payload))
        response_json = response.json()
        # Check if 'choices' exists in the response
        if 'choices' in response_json:
            response = json.loads(response_json['choices'][0]['message']['content'])
            print(F"\n\nResponse from OpenAI model: {response}")
            return response
        else:
            # Handle error case
            print(f"Error response from API: {response_json}")
            return {"error": "Failed to get valid response from API"}
