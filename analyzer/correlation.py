import pandas as pd
from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult
from core.evidence import Evidence
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
        evidence = []
        top_correlations = []
        # ----------------------------------
        # Strong Relationships
        # ----------------------------------

        for i in range(len(numeric)):
            for j in range(i + 1, len(numeric)):
                col1 = numeric[i]
                col2 = numeric[j]
                value = corr.loc[col1, col2]
                if pd.isna(value):
                    continue
                top_correlations.append({
                    "feature_a" : col1,
                    "feature_b" : col2,
                    "correlation" : float(value)
                })
                tables.append({
                    "Column A": col1,
                    "Column B": col2,
                    "Correlation": round(value, 3)
                })

                if abs(value) >= 0.80:
                    relation = ( "Strong Positive" if value > 0 else "Strong Negative"     )
                    findings.append(  f"{col1} and {col2} have {relation} correlation ({value:.2f})."  )

                    recommendations.append(f"'{col1}' and '{col2}' are highly correlated. "
                                            "Check for multicollinearity before modelling.")

                    evidence.append(
                        Evidence(
                            evidence_type="strong_correlation",
                            feature=f"{col1} ↔ {col2}",
                            value=round(float(value),3),
                            severity="high",
                            confidence=1.0,
                            description=relation,
                            metadata={
                                "column_a": col1,
                                "column_b": col2
                            }
                        )
                    )

                elif abs(value) >= 0.50:
                    relation = ( "Moderate Positive" if value > 0 else "Moderate Negative")
                    findings.append(f"{col1} and {col2} have {relation} correlation ({value:.2f}).")
                    evidence.append(
                    Evidence(
                        evidence_type="moderate_correlation",
                        feature=f"{col1} ↔ {col2}",
                        value=round(float(value),3),
                        severity="medium",
                        confidence=0.9,
                        description=relation,
                        metadata={
                            "column_a": col1,
                            "column_b": col2
                        }
                    )
                )

        charts.append({
            "type": "heatmap",
            "data": corr,
            "title": "Correlation Matrix"
        })


        top_correlations = sorted( top_correlations, key=lambda x: abs(x["correlation"]),  reverse=True)
        tables = top_correlations

        if len(findings) == 0:
            findings.append("No significant correlations detected.")

        if len(top_correlations):
            strongest = top_correlations[0]
            evidence.append(
                Evidence(
                    evidence_type="top_correlation",
                    feature=f"{strongest['feature_a']} ↔ {strongest['feature_b']}",
                    value=round( strongest["correlation"],3 ),
                    severity="high",
                    confidence=1.0,
                    description="Strongest numerical relationship"
                )
            )   

        return AnalysisResult(
            id="correlation",
            title="Correlation Analysis",
            summary=(f"Analysed {len(top_correlations)} numerical feature pairs. "
                     f"Detected {len(evidence)} meaningful relationships."),
            tables=tables,
            charts=charts,
            findings=findings,
            recommendations=recommendations,
            evidence=evidence
        )