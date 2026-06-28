"""
=========================================================
Categorical Analyzer

Enhanced categorical feature analysis.
=========================================================
"""

import pandas as pd

from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult
from utils.logger import get_logger

log = get_logger(__name__)


class CategoricalAnalyzer(BaseAnalyzer):

    def _cardinality_level(self, unique, rows):
        ratio = unique / max(rows, 1)
        if ratio > 0.90:
            return "Identifier-like"
        if unique <= 10:
            return "Low"
        if unique <= 30:
            return "Medium"
        if unique <= 100:
            return "High"
        return "Very High"

    def analyze(self, df: pd.DataFrame, profile):

        log.info("Running Categorical Analysis")

        findings = []
        recommendations = []
        tables = []
        charts = []

        categorical_cols = profile.categorical_columns

        if not categorical_cols:
            return AnalysisResult(
                id="categorical",
                title="Categorical Analysis",
                summary="No categorical columns detected."
            )

        rows = len(df)

        for col in categorical_cols:
            s = df[col].fillna("Missing")
            vc = s.value_counts(dropna=False)

            unique = int(s.nunique())
            missing = int(df[col].isna().sum())
            missing_pct = round((missing / max(rows, 1)) * 100, 2)

            top = str(vc.index[0])
            top_count = int(vc.iloc[0])
            top_pct = round((top_count / rows) * 100, 2)

            rare = vc[vc < max(5, rows * 0.01)]
            rare_count = len(rare)
            rare_pct = round((rare.sum() / rows) * 100, 2) if rare_count else 0

            level = self._cardinality_level(unique, rows)

            tables.append({
                "Column": col,
                "Cardinality": level,
                "Unique": unique,
                "Missing %": missing_pct,
                "Top Category": top,
                "Top %": top_pct,
                "Rare Categories": rare_count,
                "Rare %": rare_pct
            })

            findings.append(
                f"{col}: {level.lower()} cardinality with {unique} unique values."
            )

            if top_pct > 90:
                findings.append(
                    f"{col}: Highly imbalanced. '{top}' represents {top_pct}% of records."
                )

            elif top_pct > 70:
                findings.append(
                    f"{col}: Moderately imbalanced distribution."
                )

            if level == "Identifier-like":
                recommendations.append(
                    f"{col}: Appears to be an identifier. Exclude from statistical modelling rather than dropping automatically."
                )

            elif level in ["High", "Very High"]:
                recommendations.append(
                    f"{col}: High-cardinality categorical feature. Consider Top-N analysis, frequency encoding, target encoding or grouping infrequent categories."
                )

            if rare_pct > 5:
                recommendations.append(
                    f"{col}: Rare categories account for {rare_pct}% of observations. Consider grouping them into an 'Other' bucket."
                )

            if missing_pct > 0:
                recommendations.append(
                    f"{col}: Missing values ({missing_pct}%) should be analysed before imputation."
                )

            if unique <= 8:
                chart = "bar"
            elif unique <= 25:
                chart = "horizontal_bar"
            elif level in ["High", "Very High"]:
                chart = "top_n_bar"
            else:
                chart = "table"

            charts.append({
                "type": chart,
                "column": col,
                "top_n": 20,
                "title": f"{col} Distribution"
            })

        return AnalysisResult(
            id="categorical",
            title="Categorical Analysis",
            summary=f"Analysed {len(categorical_cols)} categorical columns with distribution, cardinality and rarity assessment.",
            findings=findings,
            recommendations=recommendations,
            tables=tables,
            charts=charts
        )
