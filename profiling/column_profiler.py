import pandas as pd
from core.column_metadata import ColumnMetadata
from utils.logger import get_logger

log = get_logger(__name__)

class ColumnProfiler:
    def profile(self, df):
        log.info("Profiling individual columns...")
        metadata = []
        total_rows = len(df)
        for col in df.columns:
            s = df[col]
            unique = s.nunique(dropna = False)
            sample = (s.dropna().head(5).tolist())
            stats = {}
            if pd.api.types.is_numeric_dtype(s):
                stats = { "mean" : float(s.mean()),
                          "std" : float(s.std()),
                          "min" : float(s.min()),
                          "max" : float(s.max()),
                          "skew" : float(s.skew()),
                          "kurtosis" : float(s.kurt())
                          }
            metadata.append(ColumnMetadata(name = col,
                                           dtype = str(s.dtype),
                                           rows = total_rows,
                                           missing_count = int(s.isna().sum()),
                                           missing_pct= round(s.isna().mean()*100, 2),
                                           unique_count= int(unique),
                                           unique_ratio= round(unique/total_rows, 4),
                                           is_numeric = pd.api.types.is_numeric_dtype(s),
                                           is_categorical = pd.api.types.is_object_dtype(s),
                                           is_datetime = pd.api.types.is_datetime64_any_dtype(s),
                                           is_binary  = (unique == 2),
                                           is_constant = (unique == 1),
                                           is_monotonic = s.is_monotonic_increasing,
                                           memory_mb = round(s.memory_usage(deep = True)/(1024*1024), 4),
                                           sample_values = sample,
                                           statistics = stats
                                        )
                            )
            
        log.info(f"{len(metadata)} columns profiled")
        return metadata