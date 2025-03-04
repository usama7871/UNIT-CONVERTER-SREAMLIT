class ConversionHistory:
    def __init__(self):
        self.history = []

    def add_conversion(self, value, unit_from, unit_to, result):
        self.history.append(f"{value} {unit_from} = {result} {unit_to}")
        if len(self.history) > 5:  # Limit history to last 5 conversions
            self.history.pop(0)

    def get_history(self):
        return self.history
