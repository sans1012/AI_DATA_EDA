import json
import re
from utils.logger import get_logger
log = get_logger(__name__)

class ResponseParser:
    @staticmethod
    def parse_json(response: str):
        if response is None:
            raise ValueError("LLM returned an empty response.")

        response = response.strip()
        response = response.replace("```json", "")
        response = response.replace("```JSON", "")
        response = response.replace("```", "")
        response = response.strip()

        start = response.find("{")
        end = response.rfind("}")
        if start == -1 or end == -1:
            log.error("No JSON object found.")
            raise ValueError("No JSON found in LLM response.")
        json_text = response[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError as e:
            log.error(f"JSON Decode Error: {e}")
            log.error(json_text)
            raise