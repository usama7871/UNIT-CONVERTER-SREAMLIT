from typing import List

class ConversionHistory:
    def __init__(self) -> None:
        self.history: List[str] = []
    
    def add_conversion(self, value: float, unit_from: str, unit_to: str, result: float) -> None:
        self.history.append(f"{value} {unit_from} = {result} {unit_to}")
        # Keep only the last 5 conversions
        if len(self.history) > 5:
            self.history.pop(0)
    
    def get_history(self) -> List[str]:
        return self.history
    
    def clear_history(self) -> None:
        self.history.clear()
