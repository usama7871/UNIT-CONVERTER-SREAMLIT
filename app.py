import streamlit as st
from converter import convert
from history import ConversionHistory
from favorites import Favorites

# Initialize conversion history and favorites
conversion_history = ConversionHistory()
favorites = Favorites()

# Title of the app
st.title("Comprehensive Unit Converter")

# Input for the value to convert
value = st.number_input("Enter the value to convert:", min_value=0.0)

# Select the category of conversion
category = st.selectbox("Select the category:", ["Length", "Weight", "Temperature", "Volume", "Area"])

# Initialize unit options based on selected category
if category == "Length":
    unit_from = st.selectbox("Select the unit to convert from:", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Inches", "Feet", "Yards"])
    unit_to = st.selectbox("Select the unit to convert to:", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Inches", "Feet", "Yards"])
elif category == "Weight":
    unit_from = st.selectbox("Select the unit to convert from:", ["Grams", "Kilograms", "Pounds", "Ounces"])
    unit_to = st.selectbox("Select the unit to convert to:", ["Grams", "Kilograms", "Pounds", "Ounces"])
elif category == "Temperature":
    unit_from = st.selectbox("Select the unit to convert from:", ["Celsius", "Fahrenheit", "Kelvin"])
    unit_to = st.selectbox("Select the unit to convert to:", ["Celsius", "Fahrenheit", "Kelvin"])
elif category == "Volume":
    unit_from = st.selectbox("Select the unit to convert from:", ["Liters", "Milliliters", "Gallons", "Pints", "Quarts"])
    unit_to = st.selectbox("Select the unit to convert to:", ["Liters", "Milliliters", "Gallons", "Pints", "Quarts"])
elif category == "Area":
    unit_from = st.selectbox("Select the unit to convert from:", ["Square Meters", "Square Kilometers", "Acres", "Hectares", "Square Feet"])
    unit_to = st.selectbox("Select the unit to convert to:", ["Square Meters", "Square Kilometers", "Acres", "Hectares", "Square Feet"])

# Layout for the conversion result
st.markdown("---")  # Horizontal line for separation
if st.button("Convert"):
    result = convert(value, unit_from, unit_to, category)
    conversion_history.add_conversion(value, unit_from, unit_to, result)
    favorites.add_favorite(value, unit_from, unit_to, result)
    st.success(f"{value} {unit_from} is equal to {result} {unit_to}")

# Display conversion history
st.subheader("Conversion History")
for entry in conversion_history.get_history():
    st.write(entry)

# Display favorites
st.subheader("Favorites")
if favorites.get_favorites():
    for entry in favorites.get_favorites():
        st.write(entry)
else:
    st.write("No favorites yet.")
    
# Option to clear favorites
if st.button("Clear Favorites"):
    favorites.clear_favorites()
    st.success("Favorites cleared.")

# Footer
st.markdown("---")
st.write("Developed by [Your Name]")  # Replace with your name or project details
