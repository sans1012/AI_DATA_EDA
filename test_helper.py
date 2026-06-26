from utils.helpers import DataLoader
from utils.helpers import DataFrameHelper

df = DataLoader.load_dataset(
    "data/netflix_titles.csv"
)

df = DataFrameHelper.optimize_memory(df)

print(df.shape)

print(
    DataFrameHelper.numeric_columns(df)
)

print(
    DataFrameHelper.categorical_columns(df)
)

print(
    DataFrameHelper.duplicate_rows(df)
)

print(
    DataFrameHelper.missing_percentage(df)
)