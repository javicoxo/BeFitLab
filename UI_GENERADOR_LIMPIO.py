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

st.title("🍽️ Generador de menú (ENTORNO LIMPIO)")
st.markdown("---")

# ======================
# SESSION STATE
# ======================
if "menu" not in st.session_state:
    st.session_state.menu = None

# ======================
# BOTÓN GENERAR MENÚ
# ======================
if st.button("🔄 Generar menú del día", use_container_width=True):
    menu = api_post(
        "/generator/generate_day",
        {"day_date": date.today().isoformat()}
    )
    st.session_state.menu = menu
    st.rerun()

# ======================
# MOSTRAR MENÚ
# ======================
menu = st.session_state.menu

if menu:
    st.markdown("### 🍽️ Menú del día")
    st.success("Menú generado correctamente")

    for meal in menu["meals"]:
        with st.container(border=True):
            st.subheader(meal["name"])

            for item in meal["items"]:
                st.write(
                    f"- **{item['food']}** — {item['grams']} g · {item['kcal']} kcal"
                )

            if st.button(
                f"🔁 Cambiar {meal['name']}",
                key=f"regen_{meal['meal_key']}"
            ):
                updated = api_post(
                    "/generator/regenerate_meal",
                    {
                        "day_date": menu["day_date"],
                        "meal_key": meal["meal_key"]
                    }
                )

                meal["items"] = updated["items"]
                st.session_state.menu = menu
                st.rerun()
