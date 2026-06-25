"""
=========================================================
Categorical Analyzer

Performs categorical feature analysis.

Checks:
- Cardinality
- Most Frequent Category
- Least Frequent Category
- Rare Categories
- Missing Values
- Suggested Visualization

Returns:
AnalysisResult
=========================================================
"""

import pandas as pd

from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult

from utils.logger import get_logger

log = get_logger(__name__)


class CategoricalAnalyzer(BaseAnalyzer):

    def analyze(self, df: pd.DataFrame, profile):

        log.info("Running Categorical Analysis")

        findings = []

        recommendations = []

        tables = []

        charts = []

        categorical_cols = profile.categorical_columns

        if len(categorical_cols) == 0:

            return AnalysisResult(
                id="categorical",
                title="Categorical Analysis",
                summary="No categorical columns detected."
            )

        for col in categorical_cols:

            series = df[col].fillna("Missing")

            value_counts = series.value_counts()

            unique = int(series.nunique())

            most_common = value_counts.index[0]

            most_common_count = int(value_counts.iloc[0])

            least_common = value_counts.index[-1]

            least_common_count = int(value_counts.iloc[-1])

            missing = int(df[col].isnull().sum())

            rare_categories = value_counts[
                value_counts < 5
            ].count()

            tables.append({

                "Column": col,

                "Unique Values": unique,

                "Most Frequent": str(most_common),

                "Frequency": most_common_count,

                "Least Frequent": str(least_common),

                "Least Frequency": least_common_count,

                "Missing": missing,

                "Rare Categories": int(rare_categories)

            })

            findings.append(

                f"{col}: {unique} unique values detected."

            )

            if unique > 50:

                recommendations.append(

                    f"{col}: High-cardinality feature. Consider grouping or encoding."

                )

            if rare_categories > 0:

                recommendations.append(

                    f"{col}: {rare_categories} rare categories detected."

                )

            if missing > 0:

                recommendations.append(

                    f"{col}: Missing values should be handled."

                )

            # Chart recommendation

            if unique <= 10:

                chart_type = "bar"

            elif unique <= 25:

                chart_type = "horizontal_bar"

            else:

                chart_type = "table"

            charts.append({

                "type": chart_type,

                "column": col,

                "title": f"{col} Distribution"

            })

        return AnalysisResult(

            id="categorical",

            title="Categorical Analysis",

            summary=f"{len(categorical_cols)} categorical columns analysed.",

            tables=tables,

            charts=charts,

            findings=findings,

            recommendations=recommendations

        )