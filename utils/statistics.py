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

    @staticmethod
    def cramers_v(df, col1, col2):
        try:
            contingency = pd.crosstab(df[col1], df[col2])
            chi2 = chi2_contingency(contingency)[0]
            n = contingency.sum().sum()
            r, k = contingency.shape
            phi2 = chi2/n
            phi2corr = max(0, phi2 - ((k-1) * (r-1))/(n-1))
            rcorr = r-((r-1) **2)/(n-1)
            kcorr = k-((k-1)**2)/(n-1)
            value = np.sqrt(phi2corr/max(1, min((kcorr-1),(rcorr-1) )))
            return float(value)
        except Exception:
            return None
        
    @staticmethod
    def strength(value):

        value = abs(value)

        if value >= 0.9:

            return "Very Strong"

        elif value >= 0.7:

            return "Strong"

        elif value >= 0.5:

            return "Moderate"

        elif value >= 0.3:

            return "Weak"

        return "Negligible"