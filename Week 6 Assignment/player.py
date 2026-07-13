import pygame

class Player:
    def __init__(self, row, col, color, id):
        self.pos = (row, col)
        self.trail_color = color - pygame.Color(200, 0, 0)
        self.territory_color = color
        self.id = id
        self.dir = (1, 0)
        self.trail = []
        self.alive = True
        self.start_pos = (row, col)
        self.territory = [self.start_pos]
        self.start_dir = (1,0)
    

    def reset(self):
        self.pos = self.start_pos
        self.dir = self.start_dir
        self.trail = []
        self.alive = True
        self.territory = [self.start_pos]
        