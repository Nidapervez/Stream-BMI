import streamlit as st
import math

# Dark Theme Styling
st.markdown(
    """
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
        }
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00ffcc !important;
        }
        div.stNumberInput>label, div.stSelectbox>label {
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Conversion Factors Dictionary
conversion_factors = {
    "Length": {
        "Meter": 1.0, "Kilometer": 1000.0, "Centimeter": 0.01, "Millimeter": 0.001,
        "Mile": 1609.34, "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254
    },
    "Mass": {
        "Kilogram": 1.0, "Gram": 0.001, "Milligram": 0.000001,
        "Pound": 0.453592, "Ounce": 0.0283495
    },
    "Temperature": {
        "Celsius": {"to_base": lambda x: x, "from_base": lambda x: x},
        "Fahrenheit": {"to_base": lambda x: (x - 32) * 5/9, "from_base": lambda x: (x * 9/5) + 32},
        "Kelvin": {"to_base": lambda x: x - 273.15, "from_base": lambda x: x + 273.15}
    },
    "Time": {
        "Second": 1.0, "Minute": 60.0, "Hour": 3600.0, "Day": 86400.0
    }
}

# Unit Conversion Function
def convert_units(value, from_unit, to_unit, category):
    factors = conversion_factors.get(category, {})
    if category == "Temperature":
        base_value = factors[from_unit]["to_base"](value)
        return factors[to_unit]["from_base"](base_value)
    else:
        return (value * factors[from_unit]) / factors[to_unit]

# Streamlit UI
st.title("🔥 Advanced Unit Converter")

# Conversion Type Selection
conversion_type = st.selectbox("Select Category", list(conversion_factors.keys()))

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    from_unit = st.selectbox("From Unit", list(conversion_factors[conversion_type].keys()))

with col2:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>⇆</h2>", unsafe_allow_html=True)

with col3:
    to_unit = st.selectbox("To Unit", list(conversion_factors[conversion_type].keys()))

# Input Value
value1 = st.number_input("Enter Value", value=1.0, step=0.1, format="%f")

# Perform Conversion
try:
    value2 = convert_units(value1, from_unit, to_unit, conversion_type)
    st.markdown(f"<h2 style='text-align: center; color: #00ffcc;'>Result: {value2:.4f}</h2>", unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"<h2 style='text-align: center; color: red;'>Error: {str(e)}</h2>", unsafe_allow_html=True)
