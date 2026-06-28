from utils.helpers import DataLoader

from agents.profiler_agent import ProfilerAgent

from analyzer.numerical import NumericalAnalyzer


df = DataLoader.load_dataset(
    "data/SampleSuperstore.csv"
)

profile = ProfilerAgent().profile(df)

analysis = NumericalAnalyzer().analyze(
    df,
    profile
)

print()

print(analysis.summary)

print()

print("Findings")

for i in analysis.findings:

    print("-", i)

print()

print("Charts")

for chart in analysis.charts:

    print(chart)

print()

print("Table")

for row in analysis.tables:

    print(row)