from llm.ollama_client import OllamaClient
from llm.prompts import PromptBuilder
from llm.parser import ResponseParser
from utils.logger import get_logger
log =get_logger(__name__)



class PlannerAgent:
    def __init__(self, model = 'qwen2.5:3b'):
        self.client = OllamaClient(model = model)
    
    def _fallback_plan(self):
        return {
            "dataset_type": "Unknown",
            "business_domain" : "Unknown",
            "possible_target": None,
            "metrics": [],
            "dimensions": [],
            "identifiers" : [],
            "recommended_analyses": [
                {
                    "analysis": "overview",
                    "priority": 1,
                    "confidence": 1.0,
                    "reason" : "Always Required"
                },
                {
                    "analysis": "data_quality",
                    "priority": 2,
                    "confidence": 1.0,
                    "reason" : "Always Required"
                },
                {
                    "analysis": "numerical",
                    "priority": 3,
                    "confidence": 1.0,
                    "reason" : "Numerical Summary"
                },
                {
                    "analysis": "categorical",
                    "priority": 4,
                    "confidence": 1.0,
                    "reason" : "Categorical Summary"
                },
                {
                    "analysis": "correlation",
                    "priority": 5,
                    "confidence": 1.0,
                    "reason" : "Correlation"
                },
                {
                    "analysis": "relationships",
                    "priority": 6,
                    "confidence": 1.0,
                    "reason" : "Relationship discovery"
                }

            ],
            "summary" : ""
        }
    
    def plan(self, dataset_profile, column_profiles):
        try:
            log.info("Generating analysis plan....")
            serialized_columns = self._serialize_columns(column_profiles)

            
            prompt = PromptBuilder.planner_prompt(dataset_profile,  serialized_columns)
            response = self.client.generate(prompt=prompt, system_prompt=PromptBuilder.planner_system_prompt())

            plan = ResponseParser.parse_json(response)

            log.info("Planner completed successfully")
            return plan
        except Exception as e:
            log.error(e)
            log.warning("Using fallback execution plan")
            return self._fallback_plan()
    
    def _serialize_columns(self, column_profiles):
        columns = []
        for col in column_profiles:
            columns.append({ "name" : col.name,
                             "dtype" : col.dtype,
                             "is_numeric" : col.is_numeric,
                             "is_binary" : col.is_binary,
                             "missing_pct" : col.missing_pct,
                             "unique_count" : col.unique_count,
                             "sample_values" : col.sample_values
                             })
        return columns