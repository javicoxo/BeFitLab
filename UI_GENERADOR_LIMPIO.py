import streamlit as st
import requests
from datetime import date

# ======================
# CONFIG API
# ======================
API_BASE = "http://127.0.0.1:8000"

def api_post(path: str, payload: dict):
    url = f"{API_BASE}{path}"
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

# ======================
# UI CONFIG
# ======================
st.set_page_config(
    page_title="BeFitLab UI",
    layout="centered"
)

st.title("🍽️ Generador de menú semanal")
st.markdown("---")

# ======================
# SESSION STATE
# ======================
if "menu" not in st.session_state:
    st.session_state.menu = None
if "week_menu" not in st.session_state:
    st.session_state.week_menu = None

# ======================
# OBJETIVOS NUTRICIONALES
# ======================
st.subheader("🎯 Objetivos diarios")
col1, col2 = st.columns(2)
with col1:
    daily_kcal = st.number_input("Kcal", min_value=1200, max_value=4000, value=2000, step=50)
    daily_protein = st.number_input("Proteínas (g)", min_value=50, max_value=250, value=120, step=5)
with col2:
    daily_carbs = st.number_input("Hidratos (g)", min_value=50, max_value=400, value=220, step=10)
    daily_fat = st.number_input("Grasas (g)", min_value=30, max_value=200, value=70, step=5)

items_per_meal = st.slider("Alimentos por comida", min_value=2, max_value=5, value=3)

# ======================
# BOTÓN GENERAR MENÚ
# ======================
if st.button("📅 Generar menú semanal", use_container_width=True):
    week_menu = api_post(
        "/generator/generate_week",
        {
            "start_date": date.today().isoformat(),
            "daily_targets": {
                "kcal": daily_kcal,
                "protein": daily_protein,
                "carbs": daily_carbs,
                "fat": daily_fat,
            },
            "items_per_meal": items_per_meal,
        },
    )
    st.session_state.week_menu = week_menu
    st.rerun()

# ======================
# MOSTRAR MENÚ
# ======================
week_menu = st.session_state.week_menu

if week_menu:
    st.markdown("### 🍽️ Menú semanal")
    st.success("Menú generado correctamente")

    for day in week_menu["days"]:
        with st.expander(f"📆 {day['day_date']}", expanded=False):
            st.caption(
                f"Totales día: {day['day_totals']['kcal']} kcal · "
                f"P {day['day_totals']['protein']} g · "
                f"H {day['day_totals']['carbs']} g · "
                f"G {day['day_totals']['fat']} g"
            )
            for meal in day["meals"]:
                with st.container(border=True):
                    st.subheader(meal["name"])
                    st.caption(
                        f"Objetivo: {meal['targets']['kcal']} kcal · "
                        f"P {meal['targets']['protein']} g · "
                        f"H {meal['targets']['carbs']} g · "
                        f"G {meal['targets']['fat']} g"
                    )
                    for item in meal["items"]:
                        st.write(
                            f"- **{item['food']}** — {item['grams']} g · "
                            f"{item['kcal']} kcal (P {item['protein']} · "
                            f"H {item['carbs']} · G {item['fat']})"
                        )
