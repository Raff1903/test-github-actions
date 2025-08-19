from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from sqlalchemy.orm import selectinload
import models, schemas
from database import get_db
from typing import List

app = FastAPI()

@app.post("/recipes", response_model=schemas.RecipeResponse)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    db_recipe = models.Recipe(
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        description=recipe.description,
        views=0
    )
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)

    for ingredient in recipe.ingredients:
        db_ingredient = models.Ingredient(name=ingredient.name, recipe_id=db_recipe.id)
        db.add(db_ingredient)
    await db.commit()

    return db_recipe

@app.get("/recipes", response_model=List[schemas.RecipeResponse])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Recipe).order_by(desc(models.Recipe.views), asc(models.Recipe.cooking_time))
    )
    recipes = result.scalars().all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetailResponse)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Recipe)
        .options(selectinload(models.Recipe.ingredients))
        .where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)

    return recipe