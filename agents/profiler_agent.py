"""
=========================================================
Profiler Agent

Analyzes any dataset and generates metadata
used by downstream AI agents.

Author : Sanskriti Jain
=========================================================
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from utils.helpers import DataFrameHelper
from utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class DatasetProfile:

    rows: int

    columns: int

    numeric_columns: List[str]

    categorical_columns: List[str]

    datetime_columns: List[str]

    duplicate_rows: int

    missing_percentage: Dict

    memory_usage_mb: float


class ProfilerAgent:

    """
    Generates dataset metadata.
    """

    def profile(
        self,
        df: pd.DataFrame
    ) -> DatasetProfile:

        log.info("Starting dataset profiling...")

        rows, cols = df.shape

        memory = (
            df.memory_usage(deep=True)
            .sum()
            / (1024 * 1024)
        )

        profile = DatasetProfile(

            rows=rows,

            columns=cols,

            numeric_columns=
            DataFrameHelper.numeric_columns(df),

            categorical_columns=
            DataFrameHelper.categorical_columns(df),

            datetime_columns=
            DataFrameHelper.datetime_columns(df),

            duplicate_rows=
            DataFrameHelper.duplicate_rows(df),

            missing_percentage=
            DataFrameHelper
            .missing_percentage(df)
            .to_dict(),

            memory_usage_mb=
            round(memory, 2)
        )

        log.info("Profiling Complete")

        return profile