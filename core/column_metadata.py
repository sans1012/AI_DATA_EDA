from dataclasses import dataclass
from typing import Any

@dataclass
class ColumnMetadata:
    name: str
    dtype: str
    rows: int
    missing_count: int
    missing_pct: float
    unique_ratio: float
    unique_count: int
    is_numeric: bool
    is_categorical: bool
    is_datetime: bool
    is_binary: bool
    is_constant: bool
    is_monotonic: bool
    memory_mb: float
    sample_values: list[Any]
    statistics: dict

