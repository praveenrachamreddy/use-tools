import requests
import json
from .base_model import BaseModel

class OllamaModel(BaseModel):
    def __init__(self, model, system_prompt, temperature=0, stop=None):
        super().__init__(model, system_prompt, temperature, stop)
        self.model_endpoint = "http://localhost:11434/api/generate"
        self.headers = {"Content-Type": "application/json"}

    def generate_text(self, prompt):
        payload = {
            "model": self.model,
            "format": "json",
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False,
            "temperature": self.temperature,
            "stop": self.stop
        }

        try:
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            
            print("REQUEST RESPONSE", request_response)
            request_response_json = request_response.json()
            response = request_response_json['response']
            response_dict = json.loads(response)

            print(f"\n\nResponse from Ollama model: {response_dict}")

            return response_dict
        except requests.RequestException as e:
            response = {"error": f"Error in invoking model! {str(e)}"}
            return response
