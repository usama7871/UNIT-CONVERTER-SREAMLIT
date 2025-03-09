from typing import List

class Favorites:
    def __init__(self) -> None:
        self.favorites: List[str] = []
    
    def add_favorite(self, value: float, unit_from: str, unit_to: str, result: float) -> None:
        self.favorites.append(f"{value} {unit_from} = {result} {unit_to}")
    
    def get_favorites(self) -> List[str]:
        return self.favorites
    
    def clear_favorites(self) -> None:
        self.favorites.clear()
    
    def remove_favorite(self, index: int) -> None:
        if 0 <= index < len(self.favorites):
            self.favorites.pop(index)
