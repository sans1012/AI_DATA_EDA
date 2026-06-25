
from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class BaseAnalyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        df: pd.DataFrame,
        profile
    ) -> Dict:
        """
        Returns structured analysis.
        """
        pass