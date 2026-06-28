from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Evidence:
    evidence_type: str
    feature:str = ""
    value: Any= None
    severity: str = "info"
    confidence: float=1.0
    description: str= ''
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return {"evidence_type" : self.evidence_type,
                "feature" : self.feature,
                "value" : self.value,
                "severity" : self.severity,
                "confidence" : self.confidence,
                "description" : self.description,
                "metadata" : self.metadata}

    def __repr__(self):
        return(f"Evidence("
               f"type = {self.evidence_type}, "
               f"feature = {self.feature}, "
               f"severity = {self.severity}) ")
    