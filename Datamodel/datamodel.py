from pydantic import BaseModel

# pydantic datamodel for data validation
class RecommendationRequest(BaseModel):
    title: str