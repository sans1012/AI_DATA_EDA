from agents.planner_agent import PlannerAgent
from agents.profiler_agent import ProfilerAgent
from profiling.column_profiler import ColumnProfiler
from analyzer.overview import OverviewAnalyzer
from analyzer.data_quality import DataQualityAnalyzer
from analyzer.numerical import NumericalAnalyzer
from analyzer.categorical import CategoricalAnalyzer
from analyzer.correlation import CorrelationAnalyzer
from analyzer.relationships import RelationshipAnalyzer
from utils.logger import get_logger
log =get_logger(__name__)

class ReportAgent:
    def __init__(self):
        self.profiler  = ProfilerAgent()
        self.column_profiler = ColumnProfiler()
        self.planner = PlannerAgent()
        self.overview = OverviewAnalyzer()
        self.quality = DataQualityAnalyzer()
        self.numerical = NumericalAnalyzer()
        self.categorical = CategoricalAnalyzer()
        self.correlation = CorrelationAnalyzer()
        self.relationships = RelationshipAnalyzer()

    def generate_report(self, df):
        log.info("Generating Complete Report")
        dataset_profile = self.profiler.profile(df)
        column_profiles = self.column_profiler.profile(df)
        planner_output = self.planner.plan(dataset_profile, column_profiles)
        overview = self.overview.analyze(df, dataset_profile)
        quality = self.quality.analyze(df, dataset_profile)
        numerical = self.numerical.analyze(df, dataset_profile)
        categorical = self.categorical.analyze(df, dataset_profile)
        correlation = self.correlation.analyze(df, dataset_profile)
        relationships = self.relationships.analyze(df, dataset_profile)

        report = {
            "dataframe" : df,
            "dataset_profile" : dataset_profile,
            "column_profile" : column_profiles,
            "planner" : planner_output,
            "overview" : overview,
            "data_quality" : quality,
            "numerical" : numerical,
            "categorical" : categorical,
            "correlation" : correlation,
            "relationships" : relationships
        }
        log.info("Report Generated Successfully")
        return report