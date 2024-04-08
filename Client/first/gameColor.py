class COLORS:
    # Class to manage and access predefined color tuples through index
    _colors = [
        (0, 0, 0),        # 0 BLACK - Represents the color black in RGB format
        (255, 0, 0),      # 1 RED - Represents the color red in RGB format
        (0, 255, 0),      # 2 GREEN - Represents the color green in RGB format
        (75, 75, 255),    # 3 BLUE - Represents a shade of blue in RGB format
        (255, 255, 0),    # 4 YELLOW - Represents the color yellow in RGB format
        (255, 255, 255),  # 5 WHITE - Represents the color white in RGB format
    ]

    def __getitem__(self, index):
        # Retrieve color tuple by index, allowing the COLOR class to be used like an array
        return self._colors[index]
    