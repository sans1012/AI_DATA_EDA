from typing import Dict
import pandas as pd
from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult
from utils.logger import get_logger
log = get_logger(__name__)

class OverviewAnalyzer(BaseAnalyzer):
    def analyze( self, df: pd.DataFrame, profile ) -> Dict:
        log.info("Running Overview Analysis")
        findings = [
            f'Dataset contains {profile.rows: ,} rows.',
            f'Dataset contains {profile.columns} columns',
            f'{len(profile.numeric_columns)} numerical columns detected.',
            f'{len(profile.categorical_columns)} categorical columns detected',
            f'{profile.duplicate_rows} duplicate rows found'
        ]
        recommendations = []
        if profile.duplicate_rows> 0:
            recommendations.append("Consider removing duplicate rows.")

        if profile.memory_usage_mb > 100:
            recommendations.append("Large Dataset detected. Consider sampling for visualizations")
        return AnalysisResult(id = 'overview',
                              title = 'Dataset Overview',
                              summary = 'Basic Dataset Statistics',
                              tables = [{
                                  'Rows':profile.rows,
                                  "Columns" : profile.columns,
                                  "Memory (MB)" : profile.memory_usage_mb,
                                  "Duplicates" : profile.duplicate_rows
                              }],
                              charts= [],
                              findings= findings,
                              recommendations= recommendations)