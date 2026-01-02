from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="BeFitLab API LIMPIA")

# =========================
# MODELOS
# =========================

class FoodItem(BaseModel):
    food: str
    grams: int
    kcal: int

class Meal(BaseModel):
    meal_key: str
    name: str
    target_kcal: int
    items: List[FoodItem]

class GenerateDayRequest(BaseModel):
    day_date: Optional[str] = None

class GenerateDayResponse(BaseModel):
    status: str
    day_date: str
    meals: List[Meal]

# =========================
# ENDPOINT
# =========================

@app.post("/generator/generate_day", response_model=GenerateDayResponse)
def generate_day(body: GenerateDayRequest):

    d = body.day_date or date.today().isoformat()

    meals = [
        Meal(
            meal_key="desayuno",
            name="Desayuno",
            target_kcal=500,
            items=[
                FoodItem(food="Avena", grams=60, kcal=228),
                FoodItem(food="Plátano", grams=120, kcal=105),
            ],
        ),
        Meal(
            meal_key="comida",
            name="Comida",
            target_kcal=800,
            items=[
                FoodItem(food="Pollo", grams=200, kcal=330),
                FoodItem(food="Arroz", grams=80, kcal=280),
            ],
        ),
    ]

    return GenerateDayResponse(
        status="ok",
        day_date=d,
        meals=meals,
    )
from fastapi import Body

class RegenerateMealRequest(BaseModel):
    day_date: str
    meal_key: str

@app.post("/generator/regenerate_meal")
def regenerate_meal(body: RegenerateMealRequest = Body(...)):
    # MOCK simple: devuelve la misma estructura con items distintos
    if body.meal_key == "desayuno":
        items = [
            {"food": "Yogur natural", "grams": 200, "kcal": 120},
            {"food": "Manzana", "grams": 150, "kcal": 80},
        ]
    else:
        items = [
            {"food": "Pescado", "grams": 180, "kcal": 220},
            {"food": "Patata", "grams": 200, "kcal": 160},
        ]

    return {
        "meal_key": body.meal_key,
        "items": items
    }
