from pydantic import BaseModel
from typing import List

class IngredientCreate(BaseModel):
    name: str

class RecipeCreate(BaseModel):
    title: str
    cooking_time: int
    description: str
    ingredients: List[IngredientCreate]

class RecipeResponse(BaseModel):
    id: int
    title: str
    cooking_time: int
    views: int

    class Config:
        orm_mode = True

class IngredientResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True

class RecipeDetailResponse(RecipeResponse):
    description: str
    ingredients: List[IngredientResponse]

    class Config:
        orm_mode = True
