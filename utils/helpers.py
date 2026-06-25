from pathlib import Path
import pandas as pd
from utils.logger import get_logger
from utils.contant import SUPPORTED_FILE_TYPES
log = get_logger(__name__)


class DataLoader:
    @staticmethod
    def load_dataset(file_path):
        """
        Reads CSV / Excel files.
        """
        suffix = Path(file_path).suffix.lower()
        if suffix not in SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"Unsupported file format : {suffix}"
            )

        log.info(f"Loading dataset : {file_path}")

        if suffix == ".csv":
            return pd.read_csv(file_path)
        return pd.read_excel(file_path)


class DataFrameHelper:

    @staticmethod
    def optimize_memory(df):
        """
        Reduce dataframe memory.
        """
        start = df.memory_usage(
            deep=True
        ).sum() / 1024**2
        for col in df.select_dtypes(
            include=["int"]
        ):
            df[col] = pd.to_numeric(
                df[col],
                downcast="integer"
            )
        for col in df.select_dtypes(
            include=["float"]
        ):
            df[col] = pd.to_numeric(
                df[col],
                downcast="float"
            )

        end = df.memory_usage(
            deep=True
        ).sum() / 1024**2

        log.info(
            f"Memory Reduced : {start:.2f} MB -> {end:.2f} MB"
        )

        return df

    @staticmethod
    def dataframe_size(df):

        return df.shape

    @staticmethod
    def missing_percentage(df):

        return (
            df.isnull()
            .mean()
            .mul(100)
            .round(2)
        )

    @staticmethod
    def duplicate_rows(df):

        return int(
            df.duplicated().sum()
        )

    @staticmethod
    def preview(df, n=5):

        return df.head(n)

    @staticmethod
    def numeric_columns(df):
        return (
            df.select_dtypes(
                include="number"
            )
            .columns
            .tolist()
        )

    @staticmethod
    def categorical_columns(df):
        return (
            df.select_dtypes(
                include=["object", "category"]
            )
            .columns
            .tolist()
        )

    @staticmethod
    def datetime_columns(df):
        return (
            df.select_dtypes(
                include=["datetime"]
            )
            .columns
            .tolist()
        )