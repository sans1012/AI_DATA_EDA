from core.base_analyzer import BaseAnalyzer
from core.analysis_result import AnalysisResult
from  utils.logger import get_logger

log = get_logger(__name__)

class SemanticProfiler(BaseAnalyzer):
    def analyze(self, df, profile):
        log.info("Running Semantic Profiling")
        metric = []
        drivers = []
        identifiers = []
        datetime_cols = []
        geo_cols = []
        customer_cols = []
        product_cols = []
        other_dimensions = []
        findings = []
        recommendations = []
        charts = []
        tables = []

        metric_keywords = [""]
