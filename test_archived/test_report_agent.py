from utils.helpers import DataLoader
from agents.report_agent import ReportAgent
df = DataLoader.load_dataset("data/netflix_titles.csv")

report = ReportAgent().generate_report(df)
print()
print(report.keys())
print()
print()
print(report['planner'])
print()
print()
print(report['overview'].summary)
