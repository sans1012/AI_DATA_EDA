from utils.helpers import DataLoader
from agents.profiler_agent import ProfilerAgent
from analyzer.data_quality import DataQualityAnalyzer

df = DataLoader.load_dataset("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
profile = ProfilerAgent().profile(df)
analysis = DataQualityAnalyzer().analyze(
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
    print('-', item)
print()
print("Table")
for row in analysis.tables:
    print(row)
