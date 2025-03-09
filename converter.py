from typing import List
from functools import lru_cache

# Conversion factors for standard categories (using a base unit approach)
conversion_factors = {
    "Length": {
        "Meters": 1,
        "Kilometers": 1000,
        "Centimeters": 0.01,
        "Millimeters": 0.001,
        "Inches": 0.0254,
        "Feet": 0.3048,
        "Yards": 0.9144
    },
    "Weight": {
        "Grams": 1,
        "Kilograms": 1000,
        "Pounds": 453.592,
        "Ounces": 28.3495
    },
    "Volume": {
        "Liters": 1,
        "Milliliters": 0.001,
        "Gallons": 3.78541,
        "Pints": 0.473176,
        "Quarts": 0.946353
    },
    "Area": {
        "Square Meters": 1,
        "Square Kilometers": 1e6,
        "Acres": 4046.86,
        "Hectares": 10000,
        "Square Feet": 0.092903
    }
}

# Extra categories using a similar approach
extra_categories = {
    "Speed": {
        # Base unit: meters per second (m/s)
        "m/s": 1,
        "km/h": 0.277778,  # 1 km/h = 0.277778 m/s
        "mph": 0.44704     # 1 mph = 0.44704 m/s
    },
    "Currency": {
        # Initially, these rates will be updated from the session state in app.py
        "USD": 1,
        "EUR": 0.9,
        "GBP": 0.8,
        "INR": 75
    }
}

def _convert_via_factor(value: float, unit_from: str, unit_to: str, factors: dict) -> float:
    """Generic conversion using a base unit approach."""
    if unit_from not in factors or unit_to not in factors:
        raise ValueError("Invalid unit for conversion.")
    # Convert to base unit then to target unit
    base_value = value * factors[unit_from]
    return base_value / factors[unit_to]

def _convert_temperature(value: float, unit_from: str, unit_to: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    if unit_from == unit_to:
        return value
    if unit_from == "Celsius":
        if unit_to == "Fahrenheit":
            return (value * 9/5) + 32
        elif unit_to == "Kelvin":
            return value + 273.15
    elif unit_from == "Fahrenheit":
        if unit_to == "Celsius":
            return (value - 32) * 5/9
        elif unit_to == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif unit_from == "Kelvin":
        if unit_to == "Celsius":
            return value - 273.15
        elif unit_to == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
    raise ValueError("Unsupported temperature conversion.")

@lru_cache(maxsize=128)
def convert(value: float, unit_from: str, unit_to: str, category: str) -> float:
    """
    Convert a single value from one unit to another.
    
    Parameters:
        value (float): The numeric value to convert.
        unit_from (str): The unit to convert from.
        unit_to (str): The unit to convert to.
        category (str): The conversion category.
        
    Returns:
        float: The converted value.
    """
    if category in conversion_factors:
        return _convert_via_factor(value, unit_from, unit_to, conversion_factors[category])
    elif category == "Temperature":
        return _convert_temperature(value, unit_from, unit_to)
    elif category in extra_categories:
        return _convert_via_factor(value, unit_from, unit_to, extra_categories[category])
    else:
        raise ValueError("Unsupported conversion category.")

def convert_batch(values: List[float], unit_from: str, unit_to: str, category: str) -> List[float]:
    """Perform batch conversion for a list of values."""
    return [convert(v, unit_from, unit_to, category) for v in values]
