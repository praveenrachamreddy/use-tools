import yaml
from models.openai_models import OpenAIModel
from models.ollama_models import OllamaModel
from toolbox.toolbox import ToolBox
from prompts.prompts import agent_system_prompt_template
from utils.logging import log_error

class Agent:
    def __init__(self, config, model_classes):
        self.tools = self.load_tools(config['tools'])
        model_config = {
            'model': config['model_name'],
            'system_prompt': config['system_prompt'],
            'temperature': config['temperature']
        }
        self.model_service = model_classes[config['model_name']](**model_config)
        self.toolbox = ToolBox()
        self.toolbox.store(self.tools)
    
    def load_tools(self, tools_list):
        tools = []
        for tool_path in tools_list:
            module_path, tool_name = tool_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[tool_name])
            tool = getattr(module, tool_name)
            tools.append(tool)
        return tools
    
    def think(self, prompt):
        try:
            tool_descriptions = self.toolbox.tools()
            agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=tool_descriptions)
            response = self.model_service.generate_text(prompt)
            return response
        except Exception as e:
            log_error(f"Error in think method: {str(e)}")
            return {"tool_choice": "no tool", "tool_input": str(e)}
    
    def work(self, prompt):
        try:
            response_dict = self.think(prompt)
            tool_choice = response_dict.get("tool_choice")
            tool_input = response_dict.get("tool_input")
            for tool in self.tools:
                if tool.__name__ == tool_choice:
                    return tool(tool_input)
            return tool_input
        except Exception as e:
            log_error(f"Error in work method: {str(e)}")
            return str(e)

def create_agent(agent_name, config_path='agents/agent_config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)['agents'][agent_name]
    model_classes = {'OpenAI': OpenAIModel, 'Ollama': OllamaModel}
    return Agent(config, model_classes)
