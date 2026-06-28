from utils.helpers import DataLoader
from profiling.column_profiler import ColumnProfiler
from profiling.semantic_reasoner import SemanticReasoner

df = DataLoader.load_dataset("data/SampleSuperstore.csv")

columns = ColumnProfiler().profile(df)
semantic = SemanticReasoner().reason(columns)

for s in semantic:

    print(
        f"{s.columns:25}"
        f"{s.role:15}"
        f"{s.confidence}"
    )

    print(s.reason)

    print("-" * 60)