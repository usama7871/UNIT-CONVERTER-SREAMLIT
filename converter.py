def convert(value, unit_from, unit_to, category):
    if category == "Length":
        if unit_from == "Meters" and unit_to == "Kilometers":
            return value / 1000
        elif unit_from == "Kilometers" and unit_to == "Meters":
            return value * 1000
        elif unit_from == "Centimeters" and unit_to == "Meters":
            return value / 100
        elif unit_from == "Millimeters" and unit_to == "Meters":
            return value / 1000
        elif unit_from == "Inches" and unit_to == "Meters":
            return value * 0.0254
        elif unit_from == "Feet" and unit_to == "Meters":
            return value * 0.3048
        elif unit_from == "Yards" and unit_to == "Meters":
            return value * 0.9144
        elif unit_from == "Meters" and unit_to == "Centimeters":
            return value * 100
        elif unit_from == "Meters" and unit_to == "Millimeters":
            return value * 1000
        elif unit_from == "Meters" and unit_to == "Inches":
            return value / 0.0254
        elif unit_from == "Meters" and unit_to == "Feet":
            return value / 0.3048
        elif unit_from == "Meters" and unit_to == "Yards":
            return value / 0.9144

    elif category == "Weight":
        if unit_from == "Grams" and unit_to == "Kilograms":
            return value / 1000
        elif unit_from == "Kilograms" and unit_to == "Grams":
            return value * 1000
        elif unit_from == "Pounds" and unit_to == "Kilograms":
            return value * 0.453592
        elif unit_from == "Ounces" and unit_to == "Grams":
            return value * 28.3495
        elif unit_from == "Kilograms" and unit_to == "Pounds":
            return value / 0.453592
        elif unit_from == "Grams" and unit_to == "Pounds":
            return value / 453.592

    elif category == "Temperature":
        if unit_from == "Celsius" and unit_to == "Fahrenheit":
            return (value * 9/5) + 32
        elif unit_from == "Fahrenheit" and unit_to == "Celsius":
            return (value - 32) * 5/9
        elif unit_from == "Celsius" and unit_to == "Kelvin":
            return value + 273.15
        elif unit_from == "Kelvin" and unit_to == "Celsius":
            return value - 273.15

    elif category == "Volume":
        if unit_from == "Liters" and unit_to == "Milliliters":
            return value * 1000
        elif unit_from == "Milliliters" and unit_to == "Liters":
            return value / 1000
        elif unit_from == "Gallons" and unit_to == "Liters":
            return value * 3.78541
        elif unit_from == "Pints" and unit_to == "Liters":
            return value * 0.473176

    elif category == "Area":
        if unit_from == "Square Meters" and unit_to == "Square Kilometers":
            return value / 1e6
        elif unit_from == "Acres" and unit_to == "Square Meters":
            return value * 4046.86

    return value  # Same unit conversion
