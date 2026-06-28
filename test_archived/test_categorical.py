from utils.helpers import DataLoader

from agents.profiler_agent import ProfilerAgent

from analyzer.categorical import CategoricalAnalyzer


df = DataLoader.load_dataset(
    "data/netflix_titles.csv"
)

profile = ProfilerAgent().profile(df)

analysis = CategoricalAnalyzer().analyze(
    df,
    profile
)

print()

print(analysis.summary)

print()

print("Findings")

for item in analysis.findings:

    print("-", item)

print()

print("Recommendations")

for item in analysis.recommendations:

    print("-", item)

print()

print("Charts")

for chart in analysis.charts:

    print(chart)

print()

print("Tables")

for row in analysis.tables:

    print(row)