class Draw:
    def __init__(self):
        self._draw = {'nomes': [], 'sorteados': []}

    @property
    def draw(self):
        return self._draw
