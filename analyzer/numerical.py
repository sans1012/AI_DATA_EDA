import pandas as pd
import numpy as np

from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult

from utils.logger import get_logger

log = get_logger(__name__)


class NumericalAnalyzer(BaseAnalyzer):

    """
    Intelligent Numerical Analysis

    Performs:

    • Descriptive Statistics
    • Distribution Detection
    • Outlier Detection
    • Zero Inflation Detection
    • Constant Column Detection
    • Missing Value Analysis
    • Smart Chart Recommendation
    """

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

            if series.empty:
                continue

            total_rows = len(df)

            unique = int(series.nunique())

            missing = int(df[col].isna().sum())

            missing_pct = round(
                missing / total_rows * 100,
                2
            )

            zero_pct = round(
                (series == 0).mean() * 100,
                2
            )

            # ----------------------------------------
            # Constant Feature
            # ----------------------------------------

            if unique == 1:

                findings.append(
                    f"{col}: Constant column detected."
                )

                recommendations.append(
                    f"{col}: Remove before modelling as it carries no predictive information."
                )

                continue

            # ----------------------------------------
            # Basic Statistics
            # ----------------------------------------

            mean = float(series.mean())

            median = float(series.median())

            std = float(series.std())

            variance = float(series.var())

            minimum = float(series.min())

            maximum = float(series.max())

            cv = 0

            if mean != 0:
                cv = std / abs(mean)

            # ----------------------------------------
            # Quartiles
            # ----------------------------------------

            q1 = float(series.quantile(0.25))

            q3 = float(series.quantile(0.75))

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            outliers = int(
                ((series < lower) | (series > upper)).sum()
            )

            outlier_pct = round(
                outliers / len(series) * 100,
                2
            )

            # ----------------------------------------
            # Distribution
            # ----------------------------------------

            skew = float(series.skew())

            kurtosis = float(series.kurt())

            if abs(skew) < 0.5:

                distribution = "Approximately Normal"

            elif skew >= 1.5:

                distribution = "Highly Right Skewed"

            elif skew >= 0.5:

                distribution = "Moderately Right Skewed"

            elif skew <= -1.5:

                distribution = "Highly Left Skewed"

            else:

                distribution = "Moderately Left Skewed"

            findings.append(

                f"{col}: {distribution}. "
                f"{outlier_pct}% observations are outliers."

            )

            # ----------------------------------------
            # Recommendations
            # ----------------------------------------

            if abs(skew) > 1:

                recommendations.append(

                    f"{col}: Highly skewed distribution detected. "
                    f"Consider log, Box-Cox or Yeo-Johnson transformation."

                )

            if outlier_pct > 5:

                recommendations.append(

                    f"{col}: {outlier_pct}% outliers detected. "
                    f"Investigate anomalies or consider RobustScaler."

                )

            if zero_pct > 70:

                recommendations.append(

                    f"{col}: Zero-inflated feature ({zero_pct}% zeros). "
                    f"Consider specialised preprocessing."

                )

            if cv > 1:

                recommendations.append(

                    f"{col}: High coefficient of variation observed "
                    f"(CV={round(cv,2)})."

                )

            if missing_pct > 20:

                recommendations.append(

                    f"{col}: {missing_pct}% missing values detected. "
                    f"Investigate before modelling."

                )

            # ----------------------------------------
            # Summary Table
            # ----------------------------------------

            summary_table.append({

                "Column": col,

                "Mean": round(mean,2),

                "Median": round(median,2),

                "Std": round(std,2),

                "Variance": round(variance,2),

                "CV": round(cv,2),

                "Min": round(minimum,2),

                "Max": round(maximum,2),

                "Q1": round(q1,2),

                "Q3": round(q3,2),

                "Missing %": missing_pct,

                "Zero %": zero_pct,

                "Unique Values": unique,

                "Skewness": round(skew,2),

                "Kurtosis": round(kurtosis,2),

                "Outliers": outliers,

                "Outlier %": outlier_pct

            })

            # ----------------------------------------
            # Intelligent Chart Selection
            # ----------------------------------------

            #
            # Binary Feature
            #

            if unique == 2:

                chart_specs.append({

                    "type": "bar",

                    "column": col,

                    "title": f"{col} Distribution"

                })

                continue

            #
            # Low-cardinality numeric
            #

            if unique <= 10:

                chart_specs.append({

                    "type": "bar",

                    "column": col,

                    "title": f"{col} Distribution"

                })

                continue

            #
            # Continuous Feature
            #

            chart_specs.append({

                "type": "histogram",

                "column": col,

                "title": f"{col} Distribution"

            })

            #
            # Only show boxplot if
            # there are sufficient unique values.
            #

            if unique > 20:

                chart_specs.append({

                    "type": "box",

                    "column": col,

                    "title": f"{col} Boxplot"

                })

            #
            # Scatter recommendation
            #

            if unique > 50:

                chart_specs.append({

                    "type": "density",

                    "column": col,

                    "title": f"{col} Density"

                })          

        # ----------------------------------------------------
        # Dataset Level Summary
        # ----------------------------------------------------

        highly_skewed = sum(
            abs(row["Skewness"]) > 1
            for row in summary_table
        )

        zero_inflated = sum(
            row["Zero %"] > 70
            for row in summary_table
        )

        high_outlier = sum(
            row["Outlier %"] > 5
            for row in summary_table
        )

        if highly_skewed:

            findings.append(

                f"{highly_skewed} numerical feature(s) are highly skewed."

            )

        if zero_inflated:

            findings.append(

                f"{zero_inflated} numerical feature(s) are zero-inflated."

            )

        if high_outlier:

            findings.append(

                f"{high_outlier} numerical feature(s) contain significant outliers."

            )

        # ----------------------------------------------------
        # Remove Duplicate Recommendations
        # ----------------------------------------------------

        recommendations = list(dict.fromkeys(recommendations))

        # ----------------------------------------------------
        # Remove Duplicate Charts
        # ----------------------------------------------------

        unique_charts = []

        seen = set()

        for chart in chart_specs:

            key = (

                chart["type"],

                chart["column"]

            )

            if key not in seen:

                unique_charts.append(chart)

                seen.add(key)

        chart_specs = unique_charts

        # ----------------------------------------------------
        # Sort Summary Table
        # ----------------------------------------------------

        summary_table = sorted(

            summary_table,

            key=lambda x: x["Outlier %"],

            reverse=True

        )

        # ----------------------------------------------------
        # Final Summary
        # ----------------------------------------------------

        summary = (

            f"{len(numeric_cols)} numerical column(s) analysed. "

            f"{highly_skewed} highly skewed, "

            f"{high_outlier} with notable outliers, "

            f"{zero_inflated} zero-inflated."

        )

        log.info("Numerical Analysis Complete.")

        return AnalysisResult(

            id="numerical",

            title="Numerical Analysis",

            summary=summary,

            tables=summary_table,

            charts=chart_specs,

            findings=findings,

            recommendations=recommendations

        ) 