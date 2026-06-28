from utils.helpers import DataLoader

from agents.profiler_agent import ProfilerAgent

from analyzer.overview import OverviewAnalyzer


df = DataLoader.load_dataset(
    "data/netflix_titles.csv"
)

profile = ProfilerAgent().profile(df)

overview = OverviewAnalyzer().analyze(
    df,
    profile
)

print(overview)