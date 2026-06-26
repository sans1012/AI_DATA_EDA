import pandas as pd
from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult
from utils.logger import get_logger

log = get_logger(__name__)

class RelationshipAnalyzer(BaseAnalyzer):
    def analyze(self, df, profile):
        log.info("Running Relationship Analysis")
        numeric_cols = profile.numeric_columns
        if len(numeric_cols)< 2:
            return AnalysisResult(id = 'relationships',
                                  title = 'Relationship analysis',
                                  summary = 'Not enough numerical columns')
        
        corr = df[numeric_cols].corr()
        findings = []
        recommendations = []
        charts = []
        tables =[]

        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                col1 = numeric_cols[i]
                col2 = numeric_cols[j]
                value = corr.loc[col1, col2]
                abs_corr = abs(value)

                if abs_corr <0.3:
                    strength = "Very Weak"
                
                elif abs_corr <0.5:
                    strength = 'Weak'

                elif abs_corr <0.7:
                    strength = 'Moderate'
                
                elif abs_corr<0.9:
                    strength = 'Strong'
                else:
                    strength = 'Very Strong'

                direction = ("Positive" if value >= 0 else "Negative")
                tables.append({ "Feature 1" : col1,
                               "Feature 2" : col2,
                               "Correlation" : round(value, 3),
                               "Strength" : strength,
                               "Direction" : direction})
                if abs_corr >= 0.5:
                    findings.append(f"{col1} and {col2} have a {strength.lower()} "
                                    f"{direction.lower()} relationship"
                                    f"({value:.2f})")
                    charts.append({
                        "type": "scatter",
                        "x" : col1,
                        "y" : col2,
                        "title": f"{col1} vs {col2}"
                    })
            
        if len(findings) == 0:
            findings.append("No meaningful feature relationships detected")

        return AnalysisResult(id = 'relationships',
                              title = "Relationship Analysis",
                              summary = "Relationship discovery between numerical variables",
                              tables = tables,
                              charts = charts,
                              findings = findings,
                              recommendations= recommendations)
    