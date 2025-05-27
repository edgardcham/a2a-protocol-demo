from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    destination: str = Field(description="The destination of the travel")
    start_date: str = Field(description="The start date of the travel")
    end_date: str = Field(description="The end date of the travel")
    budget: float = Field(description="The budget for the travel")
