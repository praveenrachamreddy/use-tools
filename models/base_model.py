import os
import yaml
from utils.get_keys import load_config

config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.yaml')
load_config(config_path)

class BaseModel:
    def __init__(self, model, system_prompt, temperature=0, stop=None):
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.stop = stop

    def generate_text(self, prompt):
        raise NotImplementedError("Subclasses should implement this method")
