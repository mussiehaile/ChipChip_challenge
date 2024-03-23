from fastapi import FastAPI
from fastapi import FastAPI, Query
from typing import Optional
from Transformation.preprocess import get_recommendation,database_operation
from Datamodel.datamodel import RecommendationRequest





app = FastAPI()


@app.get("/list_groups")
def get_groups(product_id: Optional[str] = Query(None)) -> dict:
    return {"groups": database_operation(product_id)}




@app.post("/recommendation")
def get_recommendations(request: RecommendationRequest):
    return get_recommendation(request.title)








