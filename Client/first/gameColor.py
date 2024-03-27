class COLOR:
    # Define class variables to store color values
    _colors = [
        (0, 0, 0),        # 0 BLACK
        (255, 0, 0),      # RED
        (0, 255, 0),      # GREEN
        (75, 75, 255),    # BLUE
        (255, 255, 0),    # YELLOW
        (255, 255, 255),  # WHITE
    ]

    def __getitem__(self, index):
        return self._colors[index]