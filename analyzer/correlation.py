"""
=========================================================
Correlation Analyzer

Computes correlation matrix and detects
strong relationships between numerical columns.

Returns:
AnalysisResult
=========================================================
"""

import pandas as pd

from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult

from utils.logger import get_logger

log = get_logger(__name__)


class CorrelationAnalyzer(BaseAnalyzer):

    def analyze(self, df: pd.DataFrame, profile):

        log.info("Running Correlation Analysis")

        numeric = profile.numeric_columns

        if len(numeric) < 2:

            return AnalysisResult(

                id="correlation",

                title="Correlation Analysis",

                summary="Not enough numerical columns."

            )

        corr = df[numeric].corr()

        findings = []

        recommendations = []

        tables = []

        charts = []

        # ----------------------------------

        # Strong Relationships

        # ----------------------------------

        for i in range(len(numeric)):

            for j in range(i + 1, len(numeric)):

                col1 = numeric[i]

                col2 = numeric[j]

                value = corr.loc[col1, col2]

                tables.append({

                    "Column A": col1,

                    "Column B": col2,

                    "Correlation": round(value, 3)

                })

                if abs(value) >= 0.80:

                    relation = (

                        "Strong Positive"

                        if value > 0

                        else "Strong Negative"

                    )

                    findings.append(

                        f"{col1} and {col2} have {relation} correlation ({value:.2f})."

                    )

                elif abs(value) >= 0.50:

                    relation = (

                        "Moderate Positive"

                        if value > 0

                        else "Moderate Negative"

                    )

                    findings.append(

                        f"{col1} and {col2} have {relation} correlation ({value:.2f})."

                    )

        charts.append({

            "type": "heatmap",

            "data": corr,

            "title": "Correlation Matrix"

        })

        if len(findings) == 0:

            findings.append(

                "No significant correlations detected."

            )

        return AnalysisResult(

            id="correlation",

            title="Correlation Analysis",

            summary="Correlation between numerical features.",

            tables=tables,

            charts=charts,

            findings=findings,

            recommendations=recommendations

        )