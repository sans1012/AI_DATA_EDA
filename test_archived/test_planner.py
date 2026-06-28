from utils.helpers import DataLoader
from agents.profiler_agent import ProfilerAgent
from profiling.column_profiler import ColumnProfiler
from agents.planner_agent import PlannerAgent

df = DataLoader.load_dataset("data/netflix_titles.csv")

dataset_profile = ProfilerAgent().profile(df)
column_profiles = ColumnProfiler().profile(df)
planner = PlannerAgent()

plan = planner.plan(dataset_profile,column_profiles)

print(plan)