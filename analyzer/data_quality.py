from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult

from utils.logger import get_logger

log = get_logger(__name__)


class DataQualityAnalyzer(BaseAnalyzer):

    def analyze(self, df, profile):
        log.info("Running Data Quality Analysis")
        findings = []
        recommendations = []
        quality_table = []

        missing = df.isnull().sum()

        missing_percent = (
            df.isnull().mean() * 100
        ).round(2)

        for col in df.columns:

            if missing[col] == 0:
                continue

            percent = float(missing_percent[col])

            if percent >= 50:
                severity = "High"

                recommendations.append(
                    f"{col}: Consider dropping or investigating the source."
                )

            elif percent >= 20:
                severity = "Medium"

                recommendations.append(
                    f"{col}: Imputation recommended."
                )

            else:
                severity = "Low"

            findings.append(
                f"{col} contains {percent:.2f}% missing values ({severity})."
            )

            quality_table.append({

                "Issue": "Missing Values",

                "Column": col,

                "Value": f"{percent:.2f}%",

                "Severity": severity

            })

        duplicates = int(df.duplicated().sum())

        if duplicates > 0:

            findings.append(
                f"{duplicates} duplicate rows detected."
            )

            recommendations.append(
                "Remove duplicate rows before analysis."
            )

            quality_table.append({

                "Issue": "Duplicate Rows",

                "Column": "-",

                "Value": duplicates,

                "Severity": "Medium"

            })

        for col in df.columns:

            unique = df[col].nunique(dropna=False)

            if unique == 1:

                findings.append(
                    f"{col} has only one unique value."
                )

                recommendations.append(
                    f"Remove constant column '{col}'."
                )

                quality_table.append({

                    "Issue": "Constant Column",

                    "Column": col,

                    "Value": 1,

                    "Severity": "High"

                })


        for col in profile.categorical_columns:

            unique = df[col].nunique()

            ratio = unique / len(df)

            if ratio > 0.5:

                findings.append(
                    f"{col} has high cardinality ({unique} unique values)."
                )

                recommendations.append(
                    f"Consider encoding or removing '{col}' depending on use case."
                )

                quality_table.append({

                    "Issue": "High Cardinality",

                    "Column": col,

                    "Value": unique,

                    "Severity": "Medium"

                })


        for col in profile.categorical_columns:

            empty = (df[col] == "").sum()

            if empty > 0:

                findings.append(
                    f"{col} contains {empty} empty strings."
                )

                recommendations.append(
                    f"Replace empty strings in '{col}' with NaN."
                )

                quality_table.append({

                    "Issue": "Empty Strings",

                    "Column": col,

                    "Value": empty,

                    "Severity": "Low"

                })

        if len(findings) == 0:
            findings.append(
                "No major data quality issues detected.")

        return AnalysisResult(
            id="data_quality",
            title="Data Quality",
            summary="Assessment of dataset quality.",
            tables=quality_table,
            charts=[],
            findings=findings,
            recommendations=recommendations        )