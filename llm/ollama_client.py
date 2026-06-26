import ollama
from utils.logger import get_logger
log = get_logger(__name__)

class OllamaClient:
    def __init__(self, model = "qwen2.5:3b"):
        self.model = model
    
    def generate(self, prompt: str, system_prompt: str = ""):
        try:
            response = ollama.chat(model = self.model,
                                   messages = [
                                       {
                                           "role" : "system",
                                           "content" : system_prompt
                                       },
                                       {
                                           "role" : "user",
                                           "content" : prompt
                                       }
                                   ])
            content = response['message']['content']
            log.info("LLM response generated")
            return content
        
        except Exception as e:
            log.error(e)
            raise e