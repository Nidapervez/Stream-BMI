import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight 😔 Eat nutritious foods! 🍎🥦"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight ✅ Great job! Keep staying healthy! 💪✨"
    elif 25 <= bmi < 29.9:
        return "Overweight ⚠️ Time to stay active! 🏃‍♂️🥗"
    else:
        return "Obese ❗ Consider a healthier lifestyle. 🏋️‍♀️🍏"

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #ff9966, #ff5e62);
            font-family: 'Poppins', sans-serif;
            color: #333;
        }
        .stApp {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
            text-align: center;
        }
        .result-box {
            padding: 25px;
            background: #fff;
            border-radius: 15px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
            margin-top: 25px;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-15px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #333;'>✨ Ultimate BMI Calculator ⚖️ ✨</h1>", unsafe_allow_html=True)

weight = st.number_input("⚖️ Enter your weight (kg):", min_value=1.0, step=0.1, value=50.0)
height = st.number_input("📏 Enter your height (m):", min_value=0.1, step=0.01, value=1.6)

if st.button("🔥 Calculate My BMI Now! 🔥"):
    if weight > 0 and height > 0:
        with st.spinner("🔄 Analyzing your health stats... Please wait! 🧮"):
            time.sleep(1)
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        
        st.markdown(f"""
            <div class='result-box'>
                <h2 style='color: #ff5e62;'>📊 Your BMI: <strong>{bmi:.2f}</strong></h2>
                <h3 style='color: #007bff;'>🏆 Category: <strong>{category}</strong></h3>
                <p style='font-size: 16px; color: #555;'>💡 Maintain a balanced diet and an active lifestyle for optimal health! 🌿💖</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.progress(min(bmi / 40, 1.0))
        
        fig, ax = plt.subplots()
        x = np.linspace(10, 40, 300)
        y = np.sin((x - bmi) * np.pi / 30) * 10 + 20
        ax.plot(x, y, label="BMI Trend", color="red")
        ax.axvline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("🚨 Oops! Please enter a valid weight and height to proceed. 🚨")