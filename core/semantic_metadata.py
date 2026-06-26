from dataclasses import dataclass

@dataclass
class SemanticMetadata:
    columns: str
    role: str
    confidence: str
    reason: str