import pandas as pd
from github_handler import RepoStats
from dataclasses import astuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy import stats



class Model:
    def __init__(self):
        data = pd.read_json("app.json")
        self.__data__ = data

    def calculate_similarity(self, d: RepoStats) -> float:
        test_data = astuple(d)
        inp = np.array(test_data).reshape(1, -1)
        z = cosine_similarity(inp, self.__data__)
        return np.max(z)
    
    def get_percentile(self, col_name, value) -> float:
        return stats.percentileofscore(self.__data__[col_name], value, kind='rank')

