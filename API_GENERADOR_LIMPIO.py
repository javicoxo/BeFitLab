import random
from datetime import date, timedelta
from typing import Dict, List, Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="BeFitLab API LIMPIA")

# =========================
# MODELOS
# =========================

class MacroTargets(BaseModel):
    kcal: int
    protein: float
    carbs: float
    fat: float


class FoodItem(BaseModel):
    food: str
    grams: int
    kcal: int
    protein: float
    carbs: float
    fat: float

class Meal(BaseModel):
    meal_key: str
    name: str
    targets: MacroTargets
    totals: MacroTargets
    items: List[FoodItem]

class GenerateDayRequest(BaseModel):
    day_date: Optional[str] = None
    daily_targets: Optional[MacroTargets] = None

class GenerateDayResponse(BaseModel):
    status: str
    day_date: str
    meals: List[Meal]
    day_totals: MacroTargets


class GenerateWeekRequest(BaseModel):
    start_date: Optional[str] = None
    daily_targets: MacroTargets
    meals: Optional[List[str]] = None
    meal_distribution: Optional[Dict[str, float]] = None
    items_per_meal: int = Field(3, ge=2, le=5)


class DayMenu(BaseModel):
    day_date: str
    meals: List[Meal]
    day_totals: MacroTargets


class GenerateWeekResponse(BaseModel):
    status: str
    start_date: str
    days: List[DayMenu]


MEAL_CONFIG = {
    "desayuno": "Desayuno",
    "almuerzo": "Almuerzo",
    "comida": "Comida",
    "merienda": "Merienda",
    "cena": "Cena",
}


DEFAULT_MEAL_DISTRIBUTION = {
    "desayuno": 0.25,
    "almuerzo": 0.1,
    "comida": 0.35,
    "merienda": 0.1,
    "cena": 0.2,
}


FOODS_DB = [
    {
        "food": "Avena",
        "kcal": 380,
        "protein": 13.0,
        "carbs": 62.0,
        "fat": 7.0,
        "freq_med": 0.9,
        "meal_freq": {"desayuno": 0.9, "merienda": 0.4},
    },
    {
        "food": "Yogur natural",
        "kcal": 61,
        "protein": 4.2,
        "carbs": 4.7,
        "fat": 3.3,
        "freq_med": 0.8,
        "meal_freq": {"desayuno": 0.8, "merienda": 0.7},
    },
    {
        "food": "Plátano",
        "kcal": 89,
        "protein": 1.1,
        "carbs": 23.0,
        "fat": 0.3,
        "freq_med": 0.8,
        "meal_freq": {"desayuno": 0.7, "merienda": 0.6},
    },
    {
        "food": "Manzana",
        "kcal": 52,
        "protein": 0.3,
        "carbs": 14.0,
        "fat": 0.2,
        "freq_med": 0.9,
        "meal_freq": {"desayuno": 0.6, "merienda": 0.7},
    },
    {
        "food": "Pan integral",
        "kcal": 247,
        "protein": 8.5,
        "carbs": 41.0,
        "fat": 4.2,
        "freq_med": 0.6,
        "meal_freq": {"desayuno": 0.8, "almuerzo": 0.6},
    },
    {
        "food": "Huevos",
        "kcal": 143,
        "protein": 13.0,
        "carbs": 1.1,
        "fat": 10.0,
        "freq_med": 0.5,
        "meal_freq": {"desayuno": 0.7, "cena": 0.5},
    },
    {
        "food": "Pollo",
        "kcal": 165,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6,
        "freq_med": 0.6,
        "meal_freq": {"comida": 0.8, "cena": 0.7},
    },
    {
        "food": "Pavo",
        "kcal": 135,
        "protein": 29.0,
        "carbs": 0.0,
        "fat": 1.5,
        "freq_med": 0.6,
        "meal_freq": {"comida": 0.7, "cena": 0.7},
    },
    {
        "food": "Salmón",
        "kcal": 208,
        "protein": 20.0,
        "carbs": 0.0,
        "fat": 13.0,
        "freq_med": 0.7,
        "meal_freq": {"comida": 0.5, "cena": 0.8},
    },
    {
        "food": "Merluza",
        "kcal": 90,
        "protein": 20.0,
        "carbs": 0.0,
        "fat": 1.0,
        "freq_med": 0.8,
        "meal_freq": {"comida": 0.6, "cena": 0.8},
    },
    {
        "food": "Arroz integral",
        "kcal": 362,
        "protein": 7.5,
        "carbs": 76.0,
        "fat": 2.7,
        "freq_med": 0.7,
        "meal_freq": {"comida": 0.8, "cena": 0.4},
    },
    {
        "food": "Quinoa",
        "kcal": 368,
        "protein": 14.0,
        "carbs": 64.0,
        "fat": 6.0,
        "freq_med": 0.6,
        "meal_freq": {"comida": 0.7, "cena": 0.5},
    },
    {
        "food": "Pasta integral",
        "kcal": 348,
        "protein": 13.0,
        "carbs": 70.0,
        "fat": 2.5,
        "freq_med": 0.5,
        "meal_freq": {"comida": 0.7},
    },
    {
        "food": "Patata",
        "kcal": 77,
        "protein": 2.0,
        "carbs": 17.0,
        "fat": 0.1,
        "freq_med": 0.6,
        "meal_freq": {"comida": 0.6, "cena": 0.5},
    },
    {
        "food": "Brócoli",
        "kcal": 34,
        "protein": 2.8,
        "carbs": 7.0,
        "fat": 0.4,
        "freq_med": 0.9,
        "meal_freq": {"comida": 0.7, "cena": 0.7},
    },
    {
        "food": "Ensalada mixta",
        "kcal": 20,
        "protein": 1.2,
        "carbs": 3.5,
        "fat": 0.2,
        "freq_med": 0.9,
        "meal_freq": {"comida": 0.7, "cena": 0.7},
    },
    {
        "food": "Aceite de oliva",
        "kcal": 884,
        "protein": 0.0,
        "carbs": 0.0,
        "fat": 100.0,
        "freq_med": 0.9,
        "meal_freq": {"comida": 0.5, "cena": 0.5},
    },
    {
        "food": "Frutos secos",
        "kcal": 607,
        "protein": 20.0,
        "carbs": 21.0,
        "fat": 54.0,
        "freq_med": 0.7,
        "meal_freq": {"almuerzo": 0.7, "merienda": 0.7},
    },
    {
        "food": "Hummus",
        "kcal": 166,
        "protein": 8.0,
        "carbs": 14.0,
        "fat": 9.0,
        "freq_med": 0.6,
        "meal_freq": {"almuerzo": 0.6, "merienda": 0.5},
    },
    {
        "food": "Queso fresco",
        "kcal": 98,
        "protein": 11.0,
        "carbs": 3.0,
        "fat": 4.0,
        "freq_med": 0.6,
        "meal_freq": {"almuerzo": 0.5, "merienda": 0.6},
    },
]


def _normalize_distribution(meals: List[str], distribution: Optional[Dict[str, float]]) -> Dict[str, float]:
    base = distribution or DEFAULT_MEAL_DISTRIBUTION
    filtered = {meal: base.get(meal, 0) for meal in meals}
    total = sum(filtered.values())
    if total <= 0:
        even = 1 / len(meals)
        return {meal: even for meal in meals}
    return {meal: value / total for meal, value in filtered.items()}


def _macro_scale(value: float) -> float:
    return round(value, 1)


def _food_item_from_db(food: dict, grams: int) -> FoodItem:
    factor = grams / 100
    return FoodItem(
        food=food["food"],
        grams=grams,
        kcal=int(round(food["kcal"] * factor)),
        protein=_macro_scale(food["protein"] * factor),
        carbs=_macro_scale(food["carbs"] * factor),
        fat=_macro_scale(food["fat"] * factor),
    )


def _sum_macros(items: List[FoodItem]) -> MacroTargets:
    return MacroTargets(
        kcal=sum(item.kcal for item in items),
        protein=_macro_scale(sum(item.protein for item in items)),
        carbs=_macro_scale(sum(item.carbs for item in items)),
        fat=_macro_scale(sum(item.fat for item in items)),
    )


def _select_foods_for_meal(meal_key: str, count: int) -> List[dict]:
    available = [
        food for food in FOODS_DB if meal_key in food["meal_freq"]
    ]
    if not available:
        return []
    weights = [food["freq_med"] * food["meal_freq"][meal_key] for food in available]
    return random.choices(available, weights=weights, k=count)


def _build_meal(meal_key: str, targets: MacroTargets, items_per_meal: int) -> Meal:
    selected = _select_foods_for_meal(meal_key, items_per_meal)
    if not selected:
        return Meal(
            meal_key=meal_key,
            name=MEAL_CONFIG.get(meal_key, meal_key.title()),
            targets=targets,
            totals=MacroTargets(kcal=0, protein=0, carbs=0, fat=0),
            items=[],
        )

    per_item_kcal = max(targets.kcal // len(selected), 50)
    items = []
    for food in selected:
        grams = max(int(round(per_item_kcal / food["kcal"] * 100)), 30)
        items.append(_food_item_from_db(food, grams))

    totals = _sum_macros(items)
    return Meal(
        meal_key=meal_key,
        name=MEAL_CONFIG.get(meal_key, meal_key.title()),
        targets=targets,
        totals=totals,
        items=items,
    )


def _meal_targets_from_daily(daily_targets: MacroTargets, distribution: Dict[str, float]) -> Dict[str, MacroTargets]:
    return {
        meal: MacroTargets(
            kcal=int(round(daily_targets.kcal * ratio)),
            protein=_macro_scale(daily_targets.protein * ratio),
            carbs=_macro_scale(daily_targets.carbs * ratio),
            fat=_macro_scale(daily_targets.fat * ratio),
        )
        for meal, ratio in distribution.items()
    }

# =========================
# ENDPOINT
# =========================

@app.post("/generator/generate_day", response_model=GenerateDayResponse)
def generate_day(body: GenerateDayRequest):
    d = body.day_date or date.today().isoformat()
    daily_targets = body.daily_targets or MacroTargets(
        kcal=2000,
        protein=120,
        carbs=220,
        fat=70,
    )
    meals_to_use = list(MEAL_CONFIG.keys())
    distribution = _normalize_distribution(meals_to_use, None)
    meal_targets = _meal_targets_from_daily(daily_targets, distribution)
    meals = [
        _build_meal(meal_key, meal_targets[meal_key], items_per_meal=3)
        for meal_key in meals_to_use
    ]
    day_totals = _sum_macros([item for meal in meals for item in meal.items])

    return GenerateDayResponse(
        status="ok",
        day_date=d,
        meals=meals,
        day_totals=day_totals,
    )


class RegenerateMealRequest(BaseModel):
    day_date: str
    meal_key: str
    targets: MacroTargets
    items_per_meal: int = Field(3, ge=2, le=5)


@app.post("/generator/regenerate_meal")
def regenerate_meal(body: RegenerateMealRequest = Body(...)):
    meal = _build_meal(body.meal_key, body.targets, body.items_per_meal)

    return {
        "meal_key": body.meal_key,
        "items": [item.dict() for item in meal.items],
        "totals": meal.totals.dict(),
    }


@app.post("/generator/generate_week", response_model=GenerateWeekResponse)
def generate_week(body: GenerateWeekRequest):
    start = body.start_date or date.today().isoformat()
    start_day = date.fromisoformat(start)
    meals_to_use = body.meals or list(MEAL_CONFIG.keys())
    distribution = _normalize_distribution(meals_to_use, body.meal_distribution)
    meal_targets = _meal_targets_from_daily(body.daily_targets, distribution)

    days = []
    for offset in range(7):
        day_date = start_day + timedelta(days=offset)
        meals = [
            _build_meal(meal_key, meal_targets[meal_key], body.items_per_meal)
            for meal_key in meals_to_use
        ]
        day_totals = _sum_macros([item for meal in meals for item in meal.items])
        days.append(
            DayMenu(
                day_date=day_date.isoformat(),
                meals=meals,
                day_totals=day_totals,
            )
        )

    return GenerateWeekResponse(
        status="ok",
        start_date=start,
        days=days,
    )
