from utils.helpers import DataLoader
from agents.profiler_agent import ProfilerAgent
from analyzer.correlation import CorrelationAnalyzer

df = DataLoader.load_dataset("data/winequality-red.csv")
profile = ProfilerAgent().profile(df)
analysis = CorrelationAnalyzer().analyze(df, profile)

print()
print("Analysis Summary")
print(analysis.summary)
print()

print("findings")
for i in analysis.findings:
    print("-", i)
