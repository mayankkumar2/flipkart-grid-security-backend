from github_handler import calc_repo_stats, RepoStats
from dataclasses import asdict
from fastapi import FastAPI
from pydantic import BaseModel
from model import Model

app = FastAPI()

class ReturnModel(BaseModel):
    data: RepoStats
    similarity_score: float
    data_percentiles: dict

@app.get("/get_details")
def read_root(repo: str):
    data = calc_repo_stats(repo)
    m = Model()
    sim = m.calculate_similarity(data)
    r_dict = dict()
    d = asdict(data)
    print(d)
    for k in d:
        r_dict[k] = m.get_percentile(k, d[k])
    return ReturnModel(data=data, similarity_score=sim,data_percentiles=r_dict)
