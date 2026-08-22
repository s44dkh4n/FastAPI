from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Annotated, Literal
from config.citytier import tier_1_cities,tier_2_cities
class UserInfo(BaseModel):
    age: Annotated[int, Field(..., description="Age of the Person.", examples=[30, 46])]
    height: Annotated[float, Field(..., description="Height of Person in meters", gt=0)]
    weight: Annotated[float, Field(..., description="Weight of Person in kg", ge=1)]
    income: Annotated[float, Field(..., description="Income of the person in LPA.", examples=[1.42], gt=0)]
    smoker: Annotated[bool, Field(description="True if Smoker else False")]
    city: Annotated[str, Field(..., description="City where the person lives", examples=["Mumbai"])]
    occupation: Annotated[Literal["freelancer", "buisness_owner", "government_job", "retired", "unemployed", "private_job", "student"], Field(..., description="Occupation of Person")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property 
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif 25 <= self.age <= 45:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def city_tier(self) -> int:
        city = self.city
        if city in tier_1_cities:
            return 1
        elif city in tier_2_cities:
            return 2
        else:
            return 3

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()
         
