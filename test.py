from llm.ollama_client import OllamaClient

client = OllamaClient()

print(client.generate("Say hello"))