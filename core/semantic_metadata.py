from dataclasses import dataclass, field
from typing import List


@dataclass
class SemanticMetadata:

    # Basic Information
    column: str
    dtype: str = ""

    # Semantic Classification
    semantic_type: str = "unknown"
    role: str = "unknown"
    confidence: float = 0.0

    # Flags
    is_metric: bool = False
    is_dimension: bool = False
    is_identifier: bool = False
    is_target: bool = False
    is_datetime: bool = False
    is_geography: bool = False
    is_text: bool = False
    is_binary: bool = False
    is_high_cardinality: bool = False

    # Statistics
    unique_count: int = 0
    unique_ratio: float = 0.0
    missing_pct: float = 0.0
    sample_values: List = field(default_factory=list)

    # Visualization
    recommended_chart: str = ""

    # Statistics to perform
    statistical_tests: List[str] = field(default_factory=list)

    # Explanation
    notes: List[str] = field(default_factory=list)

    def to_dict(self):

        return {

            "column": self.column,
            "dtype": self.dtype,

            "semantic_type": self.semantic_type,
            "role": self.role,
            "confidence": self.confidence,

            "is_metric": self.is_metric,
            "is_dimension": self.is_dimension,
            "is_identifier": self.is_identifier,
            "is_target": self.is_target,
            "is_datetime": self.is_datetime,
            "is_geography": self.is_geography,
            "is_text": self.is_text,
            "is_binary": self.is_binary,
            "is_high_cardinality": self.is_high_cardinality,

            "unique_count": self.unique_count,
            "unique_ratio": self.unique_ratio,
            "missing_pct": self.missing_pct,
            "sample_values": self.sample_values,

            "recommended_chart": self.recommended_chart,
            "statistical_tests": self.statistical_tests,

            "notes": self.notes

        }

    def __repr__(self):

        return (
            f"SemanticMetadata("
            f"{self.column}, "
            f"{self.role}, "
            f"{self.confidence:.2f})"
        )