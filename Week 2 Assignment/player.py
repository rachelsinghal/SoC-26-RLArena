class Player:
    def __init__(self, row, col, color, id):
        self.pos = (row, col)
        self.color = color
        self.id = id
        self.dir = (1, 0)
        self.trail = []
        self.alive = True
        self.start_pos = (row, col)
        self.start_dir = (1,0)

    def reset(self):
        self.pos = self.start_pos
        self.dir = self.start_dir
        self.trail = []
        self.alive = True
        