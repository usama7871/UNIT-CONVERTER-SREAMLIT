import streamlit as st
import pandas as pd
import random
from converter import convert, conversion_factors, extra_categories
from history import ConversionHistory
from favorites import Favorites
from logger import get_logger

logger = get_logger()

def init_state():
    if "conversion_history" not in st.session_state:
        st.session_state.conversion_history = ConversionHistory()
    if "favorites" not in st.session_state:
        st.session_state.favorites = Favorites()
    if "advanced_mode" not in st.session_state:
        st.session_state.advanced_mode = False
    if "currency_rates" not in st.session_state:
        st.session_state.currency_rates = {"USD": 1, "EUR": 0.9, "GBP": 0.8, "INR": 75}

# Initialize session state keys if missing.
init_state()

st.set_page_config(page_title="Amazing Unit Converter", layout="wide")
st.title("Amazing Unit Converter")

# Sidebar: History, Favorites, Export Options & Reset App
with st.sidebar:
    st.header("History & Favorites")
    
    st.subheader("Conversion History")
    history = st.session_state.conversion_history.get_history()
    if history:
        for idx, entry in enumerate(history, start=1):
            st.write(f"{idx}. {entry}")
    else:
        st.info("No conversions yet.")
    
    if st.button("Clear History"):
        st.session_state.conversion_history.clear_history()
        st.success("Conversion history cleared.")
    
    st.subheader("Favorites")
    favorites_list = st.session_state.favorites.get_favorites()
    if favorites_list:
        for idx, entry in enumerate(favorites_list, start=1):
            st.write(f"{idx}. {entry}")
    else:
        st.info("No favorites yet.")
    
    if st.button("Clear Favorites"):
        st.session_state.favorites.clear_favorites()
        st.success("Favorites cleared.")
    
    if st.button("Export History as CSV"):
        if history:
            df = pd.DataFrame(history, columns=["Conversion"])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='conversion_history.csv',
                mime='text/csv'
            )
        else:
            st.info("No history to export.")
    
    # Reset App Button: Clear all session state and stop further execution.
    if st.button("Reset App"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("App reset. Please refresh your browser.")
        st.stop()  # Stop further execution after reset.

# Use a safe accessor for advanced_mode.
advanced = st.checkbox("Show Advanced Options", value=st.session_state.get("advanced_mode", False))
st.session_state.advanced_mode = advanced
# Main conversion form
with st.form(key="conversion_form"):
    col1, col2 = st.columns(2)
    with col1:
        value = st.number_input("Enter the value to convert:", min_value=0.0, format="%.4f")
    with col2:
        # Combine all standard, extra, and Temperature categories
        all_categories = list(conversion_factors.keys()) + list(extra_categories.keys()) + ["Temperature"]
        category = st.selectbox("Select the category:", all_categories)
    
    # Determine the list of units based on category
    if category in conversion_factors:
        units = list(conversion_factors[category].keys())
    elif category in extra_categories:
        units = list(extra_categories[category].keys())
    elif category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
    else:
        units = []
    
    # Get unit selections without binding them to session_state keys
    unit_from = st.selectbox("Convert from:", units, index=0)
    unit_to = st.selectbox("Convert to:", units, index=1)
    
    # Advanced: Batch conversion input (comma-separated values)
    if advanced:
        batch_input = st.text_input("Batch Conversion (comma-separated values)", value="")
    else:
        batch_input = ""
    
    # Provide two submit buttons: one for swapping, one for normal conversion.
    swap_clicked = st.form_submit_button("Swap Units")
    convert_clicked = st.form_submit_button("Convert")

# Update Currency rates if needed
if category == "Currency":
    extra_categories["Currency"] = st.session_state.currency_rates
    if st.button("Refresh Currency Rates"):
        new_rates = {"USD": 1}
        for cur, rate in st.session_state.currency_rates.items():
            if cur != "USD":
                change = 1 + random.uniform(-0.05, 0.05)  # ±5% variation
                new_rates[cur] = round(rate * change, 4)
        st.session_state.currency_rates = new_rates
        extra_categories["Currency"] = new_rates
        st.success("Currency rates updated!")
        st.write("New Rates:", new_rates)

# Conversion logic after form submission
if convert_clicked or swap_clicked:
    try:
        # Batch conversion handling
        if batch_input and batch_input.strip():
            values = [float(x.strip()) for x in batch_input.split(",") if x.strip()]
            if swap_clicked:
                results = [convert(v, unit_to, unit_from, category) for v in values]
                st.success("Batch Conversion Results (Swapped):")
                for v, res in zip(values, results):
                    st.write(f"{v} {unit_to} = {res} {unit_from}")
                    st.session_state.conversion_history.add_conversion(v, unit_to, unit_from, res)
                    st.session_state.favorites.add_favorite(v, unit_to, unit_from, res)
                logger.info("Performed batch conversion with swapped units.")
            else:
                results = [convert(v, unit_from, unit_to, category) for v in values]
                st.success("Batch Conversion Results:")
                for v, res in zip(values, results):
                    st.write(f"{v} {unit_from} = {res} {unit_to}")
                    st.session_state.conversion_history.add_conversion(v, unit_from, unit_to, res)
                    st.session_state.favorites.add_favorite(v, unit_from, unit_to, res)
                logger.info("Performed batch conversion.")
        else:
            # Single conversion
            if swap_clicked:
                result = convert(value, unit_to, unit_from, category)
                st.success(f"{value} {unit_to} is equal to {result} {unit_from} (Swapped)")
                st.session_state.conversion_history.add_conversion(value, unit_to, unit_from, result)
                st.session_state.favorites.add_favorite(value, unit_to, unit_from, result)
                logger.info("Performed single conversion with swapped units.")
            else:
                result = convert(value, unit_from, unit_to, category)
                st.success(f"{value} {unit_from} is equal to {result} {unit_to}")
                st.session_state.conversion_history.add_conversion(value, unit_from, unit_to, result)
                st.session_state.favorites.add_favorite(value, unit_from, unit_to, result)
                logger.info("Performed single conversion.")
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        st.error(f"Conversion error: {e}")

# Option to show conversion table for the current category
if st.checkbox("Show Conversion Table for this Category"):
    if category in conversion_factors:
        st.write("Conversion Factors:")
        st.table(pd.DataFrame(list(conversion_factors[category].items()), columns=["Unit", "Factor"]))
    elif category in extra_categories:
        st.write("Conversion Factors:")
        st.table(pd.DataFrame(list(extra_categories[category].items()), columns=["Unit", "Factor"]))
    elif category == "Temperature":
        st.write("Available Temperature Units: Celsius, Fahrenheit, Kelvin")
    else:
        st.info("No conversion table available for this category.")

# Display favorites with option to remove individual entries
st.subheader("Favorites")
favorites_list = st.session_state.favorites.get_favorites()
if favorites_list:
    for idx, entry in enumerate(favorites_list):
        col_a, col_b = st.columns([8, 2])
        with col_a:
            st.write(entry)
        with col_b:
            if st.button("Remove", key=f"fav_{idx}"):
                st.session_state.favorites.remove_favorite(idx)
                st.success("Favorite removed.")
else:
    st.info("No favorites yet.")

st.markdown("---")
st.write("Developed by Usama s/o MUHAMMAD ABDULLAH")
st.write("Contact: kusamakhan1234@gmail.com")