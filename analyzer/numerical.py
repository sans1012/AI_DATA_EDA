"""
=========================================================
Numerical Analyzer

Performs numerical feature analysis.

Checks:
- Summary Statistics
- Missing Values
- Skewness
- Kurtosis
- Outliers (IQR)
- Distribution Type

Returns:
AnalysisResult

=========================================================
"""

import pandas as pd

from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult

from utils.logger import get_logger

log = get_logger(__name__)


class NumericalAnalyzer(BaseAnalyzer):

    def analyze(self, df: pd.DataFrame, profile):

        log.info("Running Numerical Analysis")

        findings = []

        recommendations = []

        summary_table = []

        chart_specs = []

        numeric_cols = profile.numeric_columns

        if len(numeric_cols) == 0:

            return AnalysisResult(
                id="numerical",
                title="Numerical Analysis",
                summary="No numerical columns detected."
            )

        for col in numeric_cols:

            series = df[col].dropna()

            if len(series) == 0:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            outliers = int(
                ((series < lower) | (series > upper)).sum()
            )

            skew = float(series.skew())

            kurtosis = float(series.kurt())

            # Distribution

            if abs(skew) < 0.5:

                distribution = "Approximately Normal"

            elif skew > 0.5:

                distribution = "Right Skewed"

            else:

                distribution = "Left Skewed"

            findings.append(

                f"{col}: {distribution}, {outliers} outliers detected."

            )

            if abs(skew) > 1:

                recommendations.append(

                    f"{col}: Consider log transformation if required for ML."

                )

            summary_table.append({

                "Column": col,

                "Mean": round(series.mean(), 2),

                "Median": round(series.median(), 2),

                "Std": round(series.std(), 2),

                "Min": round(series.min(), 2),

                "Max": round(series.max(), 2),

                "Skewness": round(skew, 2),

                "Kurtosis": round(kurtosis, 2),

                "Outliers": outliers

            })

            # Chart Specification

            chart_specs.append({

                "type": "histogram",

                "column": col,

                "title": f"{col} Distribution"

            })

            chart_specs.append({

                "type": "box",

                "column": col,

                "title": f"{col} Boxplot"

            })

        return AnalysisResult(

            id="numerical",

            title="Numerical Analysis",

            summary=f"{len(numeric_cols)} numerical columns analysed.",

            tables=summary_table,

            charts=chart_specs,

            findings=findings,

            recommendations=recommendations

        )