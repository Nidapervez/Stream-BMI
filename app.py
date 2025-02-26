import streamlit as st
import math
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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

# ---------------------------
# 1. Unit Converter Section
# ---------------------------
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

def convert_units(value, from_unit, to_unit, category):
    factors = conversion_factors.get(category, {})
    if category == "Temperature":
        base_value = factors[from_unit]["to_base"](value)
        return factors[to_unit]["from_base"](base_value)
    else:
        return (value * factors[from_unit]) / factors[to_unit]

st.title("🔥 Advanced Unit Converter")
conversion_type = st.selectbox("Select Category", list(conversion_factors.keys()))
col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    from_unit = st.selectbox("From Unit", list(conversion_factors[conversion_type].keys()))
with col2:
    st.markdown("<h2 style='text-align: center; color: #00ffcc;'>⇆</h2>", unsafe_allow_html=True)
with col3:
    to_unit = st.selectbox("To Unit", list(conversion_factors[conversion_type].keys()))
value1 = st.number_input("Enter Value", value=1.0, step=0.1, format="%f")
try:
    value2 = convert_units(value1, from_unit, to_unit, conversion_type)
    st.markdown(f"<h2 style='text-align: center; color: #00ffcc;'>Result: {value2:.4f}</h2>", unsafe_allow_html=True)
except Exception as e:
    st.markdown(f"<h2 style='text-align: center; color: red;'>Error: {str(e)}</h2>", unsafe_allow_html=True)

# ---------------------------
# 2. Chatbot Integration Section
# ---------------------------
st.header("💬 Website Chatbot")
st.write("Ask any question related to our website and unit converter features:")

# Sample website content data (expand with your real website content)
website_data = [
    {"section": "Home", "content": "Welcome to our advanced unit converter. Explore our features for length, mass, temperature, and time conversions."},
    {"section": "Length Conversion", "content": "Convert meters, kilometers, miles, and more with precise conversion factors."},
    {"section": "Mass Conversion", "content": "Accurately convert kilograms, grams, pounds, and other mass units."},
    {"section": "Temperature Conversion", "content": "Easily convert between Celsius, Fahrenheit, and Kelvin using our tool."},
    {"section": "Time Conversion", "content": "Quickly convert seconds, minutes, hours, and days with our unit converter."},
]

# Use st.cache_resource for model loading (load your fine-tuned model if available)
@st.cache_resource
def load_model():
    try:
        # Try to load your fine-tuned model (ensure the folder "fine_tuned_model" exists)
        return SentenceTransformer("fine_tuned_model")
    except Exception:
        # Fallback to the pre-trained model if fine-tuned model is not found
        return SentenceTransformer('all-MiniLM-L6-v2')

# Use st.cache_data for computing embeddings
@st.cache_data
def compute_embeddings(contents):
    return model.encode(contents)

model = load_model()
contents = [item['content'] for item in website_data]
content_embeddings = compute_embeddings(contents)

def is_conversion_query(query):
    # Check if the query includes digits and unit keywords
    unit_keywords = ['m', 'cm', 'km', 'mm', 'inch', 'foot', 'yard', 'mile']
    return any(char.isdigit() for char in query) and any(keyword in query.lower() for keyword in unit_keywords)

def get_response(user_query, threshold=0.35):
    # You might want to experiment with threshold values based on your training data
    query_embedding = model.encode([user_query])
    similarities = cosine_similarity(query_embedding, content_embeddings)
    best_match_idx = int(np.argmax(similarities))
    best_similarity = similarities[0][best_match_idx]
    
    # Uncomment to debug similarity scores:
    # st.write("Similarity Scores:", similarities.tolist())
    
    if best_similarity < threshold:
        return "I'm sorry, I couldn't find a relevant answer. Can you please rephrase your question?"
    return website_data[best_match_idx]['content']

user_question = st.text_input("Your question about the website:")

if user_question:
    if is_conversion_query(user_question):
        st.markdown("It looks like you're trying to perform a unit conversion. Please use the unit converter above.")
    else:
        response = get_response(user_question)
        st.markdown(f"**Answer:** {response}", unsafe_allow_html=True)
