class COLOR:
    # Define class variables to store color values
    _colors = [
        (255, 0, 0),      # 0 RED
        (0, 255, 0),      # 1 GREEN
        (75, 75, 255),    # 2 BLUE
        (255, 255, 0),    # 3 YELLOW
        (255, 255, 255),  # 4 WHITE
        (0, 0, 0)         # 5 BLACK
    ]

    def __getitem__(self, index):
        return self._colors[index]