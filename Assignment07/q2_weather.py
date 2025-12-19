from langchain_openai import ChatOpenAI
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# ---------------- ENV ----------------
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ---------------- LLM (LM Studio) ----------------
llm = ChatOpenAI(
    model="google/gemma-3n-e4b",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    temperature=0.3
)

# ---------------- WEATHER LOGIC ----------------
def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

st.set_page_config(page_title="Weather App", page_icon="🌦")

# ---------------- LOGIN PAGE ----------------
if not st.session_state.login:
    st.title("🔐 Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == password and user != "":
            st.session_state.login = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------------- MAIN APP ----------------
else:
    st.title("🌦 Weather Application")

    # ---------- SIDEBAR ----------
    with st.sidebar:
        st.header("🌍 City Input")
        city = st.text_input("Enter city name")
        get_weather_btn = st.button("Get Weather")
        st.markdown("---")

        if st.button("Logout"):
            st.session_state.login = False
            st.rerun()

    # ---------- MAIN OUTPUT ----------
    if get_weather_btn:
        if not city:
            st.warning("Please enter a city name")
        else:
            weather = get_weather(city)

            if weather is None:
                st.error("City not found or API error")
            else:
                temp = weather["temp"]
                humidity = weather["humidity"]
                wind = weather["wind"]
                description = weather["description"]

                llm_msg = f"""
Weather details:
- Temperature: {temp} °C
- Humidity: {humidity} %
- Wind Speed: {wind} m/s
- Condition: {description}

Explain the weather in simple bullet points for a normal user.
"""

                result = llm.invoke(llm_msg)

                st.subheader(f"🌤 Current Weather in {city}")
                st.write(f"**Temperature:** {temp} °C")
                st.write(f"**Humidity:** {humidity} %")
                st.write(f"**Wind Speed:** {wind} m/s")
                st.write(f"**Condition:** {description}")

                st.subheader("🤖 AI Explanation")
                st.write(result.content)
