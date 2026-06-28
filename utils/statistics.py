import numpy as np
import pandas as pd
from scipy.stats import(pearsonr, spearmanr, f_oneway, chi2_contingency)

class StatisticalTests:
    @staticmethod
    def pearson(x, y):
        try:
            corr, p = pearsonr(x, y)
            return {"correlation": float(corr),
                    "p_value": float(p)}
        except Exception as e:
            return None

    @staticmethod
    def anova(df, numeric_col, category_col):
        try:
            groups = []
            for _, g in df.groupby(category_col):
                values = g[numeric_col].dropna()
                if len(values)>1:
                    groups.append(values)
            if len(groups)<2:
                return None
            
            f_stat, p_value = f_oneway(groups)
            return {"f_statistic": float(f_stat),
                    "p_value": float(p_value),
                    "significant": p_value<0.05
            }
        
        except Exception as e:
            return None
        
    @staticmethod
    def chi_square(df, col1, col2):
        try:
            contingency = pd.crosstab(df[col1], df[col2])
            chi2, p, dof, expected = chi2_contingency(contingency)
            return {"chi2": float(chi2),
                    "p_value":float(p),
                    "dof" : int(dof),
                    "significant": p<0.05,
                    "contingency": contingency}
        except Exception as e:
            return None