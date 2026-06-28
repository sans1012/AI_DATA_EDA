from utils.helpers import DataLoader

from agents.profiler_agent import (
    ProfilerAgent
)

df = DataLoader.load_dataset(
    "data/netflix_titles.csv"
)

agent = ProfilerAgent()

profile = agent.profile(df)

print(profile)