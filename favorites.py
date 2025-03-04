class Favorites:
    def __init__(self):
        self.favorites = []

    def add_favorite(self, value, unit_from, unit_to, result):
        self.favorites.append(f"{value} {unit_from} = {result} {unit_to}")

    def get_favorites(self):
        return self.favorites

    def clear_favorites(self):
        self.favorites.clear()
