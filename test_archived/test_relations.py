from utils.helpers import DataLoader
from agents.profiler_agent import ProfilerAgent
from analyzer.relationships import RelationshipAnalyzer

df = DataLoader.load_dataset('data/winequality-red.csv')
profile = ProfilerAgent().profile(df)
analysis = RelationshipAnalyzer().analyze(df, profile)

print()
print(analysis.summary)
print()
print("Findings")
for f in analysis.findings:
    print("-", f)
print()
print("Charts")
for c in analysis.charts:
    print(c)