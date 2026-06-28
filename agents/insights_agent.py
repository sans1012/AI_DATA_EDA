import json
from llm.ollama_client import OllamaClient
from llm.prompts import PromptBuilder
from llm.parser import ResponseParser
from utils.logger import get_logger

log = get_logger(__name__)

class InsightAgent:
    def __init__(self, model = "qwen2.5:3b"):
        self.client = OllamaClient(model = model)

    def generate(self, report):
        log.info("Generating AI Insights...")
        evidence = report.get("evidence", [])
        evidence_json = []
        for item in evidence:
            if hasattr(item, "to_dict"):
                evidence_json.append(item.to_dict())
            else:
                evidence_json.append(item)

        prompt = PromptBuilder.insight_prompt( report,evidence_json)
        response = self.client.generate( prompt=prompt, system_prompt=PromptBuilder.insight_system_prompt())

        try:
            parsed = ResponseParser.parse_json(response)
            log.info("AI Insights Generated Successfully.")
            return parsed

        except Exception as e:
            log.warning(  "Unable to parse Insight JSON : %s", str(e)  )
            return {
                "executive_summary": response,
                "key_findings": [],
                "business_recommendations": [],
                "data_quality_risks": [],
                "ml_readiness": "",
                "feature_engineering": [],
                "next_steps": []
            }
        
    def _build_prompt(self, report, evidence):
        planner = report.get("planner", {})
        profile = report.get("dataset_profiler")
        prompt = f""""  DATASET PROFILE
                        
                        Rows: {profile.rows}
                        
                        Columns: {profile.columns}
                        
                        Dataset Type: {planner.get("dataset_type", "Unknown")}
                        
                        Business Domain: {planner.get("business_domain", "Unknown")}

                        Possible Target: {planner.get("possible_target", "Unknown")}
                        
                        Business Metrics: 
                        {planner.get('metrics', [])}

                        Dimensions: 
                        {planner.get('dimensions', [])}

                        STRUCTURED EVIDENCE
                        {json.dumps(evidence, indent = 2)}

                        Generate a JSON Response having exactly these keys.
                        {{
                        "executive_summary" : "",
                        "key_findings" : [],
                        "business_recommendations" : [],
                        "ml_readiness" : "",
                        "next_steps" : []
                        }}

                        Rules:
                        1. Never invent Facts.
                        2. Dont assume what you don't know.
                        3. Only use supplied evidence.
                        4. Explain observations in business language. 
                        5. Avoid repeating statistics. 
                        6. Mention important risks. 
                        7. Mention Feature Engineering suggestions.
                        8. Mention modelling readiness. 

                        Return ONLY JSON.
                        """
        return prompt
    

    def _system_prompt(self):
        return  """You are Senior Principle Data Scientist. 
                    You are analysing outputs from an automated EDA System.
                    Your job is NOT to compute statistics
                    Your job is to reason over supplied evidence
                    Provide concise business insights
                    Do not hallucinate.
                    Do not share anything you are not confidence about. 
                    Never invent columns. 
                    Always return valid JSON. 
                """