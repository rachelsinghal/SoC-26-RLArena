from constants import *
import numpy as np

class Game:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self,player):
        self.players.append(player)
        row, col = player.start_pos
        self.grid[row][col] = player.id

    def update(self):
        # compute all next positions
        next_pos = {}
        for player in self.players:
            next_pos[player] = (player.pos[0] + player.dir[0], player.pos[1] + player.dir[1])
        # head-on — same target cell kills both
        if next_pos[self.players[0]] == next_pos[self.players[1]]:
            for player in self.players:
                player.alive = False
        for player in self.players:
            if 0<= next_pos[player][0] < 80 and 0<= next_pos[player][1] < 80 and player.dir!= (0,0):
                if self.grid[next_pos[player][0]][next_pos[player][1]] != 0:
                    player.alive = False
            else:
                player.dir = (0,0)
                next_pos[player] = player.pos
            #move the players who survived
            if player.alive: 
                if next_pos[player] != player.pos:
                    player.trail.append(player.pos) 
                    player.pos = next_pos[player]
                    self.grid[next_pos[player][0], next_pos[player][1]] = player.id


    def reset(self):
        for player in self.players:
            player.reset()
        self.grid = np.zeros((self.rows, self.cols), dtype=int)