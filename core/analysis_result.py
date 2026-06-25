from dataclasses import dataclass, field
from typing import Any

@dataclass
class AnalysisResult:
    id:str
    title:str
    summary:str
    tables: list[Any] = field(default_factory= list)
    charts: list[dict] = field(default_factory= list)
    findings: list[str] = field(default_factory= list)
    recommendations: list[str] = field(default_factory= list)

    