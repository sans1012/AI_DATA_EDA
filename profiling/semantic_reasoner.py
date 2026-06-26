from core.semantic_metadata import SemanticMetadata
from utils.logger import get_logger

log = get_logger(__name__)

class SemanticReasoner:
    def reason(self, columns_metadata):
        log.info("Running Semantic Reasoner")
        semantic_results = []
        for column in columns_metadata:
            scores = {"Identifier": 0,
                      "Metric" : 0,
                      "Dimension": 0,
                      "Target": 0,
                      "Datetime": 0,
                      "Text" : 0}
            reasons = []
            if column.unique_ratio  > 0.95:
                scores['Identifier'] +=60
                reasons.append("Nearly every value is unique")

            if "id" in column.name.lower():
                scores['Identifier'] +=30
                reasons.append(f"{column} suggests as identifier")
            
            if column.is_numeric:
                scores['Metric'] +=40
                reasons.append("Numeric Column")
            
            if (column.statistics and column.statistics.get("std", 0)>0):
                scores['Metric'] +=20
                reasons.append("Continuous numeric values.")
            
            if column.is_binary:
                scores['Target'] +=50
                reasons.append("Binary Feature")
            
            if column.unique_count  ==2:
                scores['Target'] +=20
            
            if column.is_datetime:
                scores['Datetime'] +=100
                reasons.append("Datetime detected")
            
            if (column.is_categorical  and column.unique_ratio>0.7):
                scores['Text'] +=40
                reasons.append("High-cardinality text")
            
            role = max(scores, key = scores.get)
            confidence = round(scores[role]/100, 2)
            semantic_results.append(SemanticMetadata(columns= column.name,
                                                     role = role,
                                                     confidence= confidence,
                                                     reason = " | ".join(reasons)))
        log.info("Semantic Reasoning Complete.")
        return semantic_results