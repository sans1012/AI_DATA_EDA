from utils.helpers import DataLoader
from profiling.column_profiler import ColumnProfiler

df = DataLoader.load_dataset("data/winequality-red.csv" )
columns = ColumnProfiler().profile(df)

for col in columns:
    print()
    print(col.name)
    print(col)