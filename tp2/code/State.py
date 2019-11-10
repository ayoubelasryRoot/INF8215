import numpy as np
import math
import copy
from collections import deque

class State:
    
    def __init__(self, pos):

        self.pos = np.array(pos)

        self.c = self.d = self.prev = None
        
        self.nb_moves = 0
        self.score = 0
        
        # TODO
        self.rock = None

    def move(self, c, d):
        s = State(self.pos)
        s.prev = self
        s.pos[c] += d
        s.c = c
        s.d = d
        s.nb_moves = self.nb_moves + 1
        s.rock = self.rock
        return s

    def put_rock(self, rock_pos):
        s = State(self.pos)
        s.nb_moves = self.nb_moves
        s.rock = rock_pos
        return s
            
    def estimee1(self):
        # TODO
        caseFinal = 4 # 6 cases - 2 de longueurs
        return  caseFinal - self.pos[0]
    
    def score_state(self, rh):
        if self.prev != None and self.c == self.prev.c and self.prev.d == self.d * -1:
            return float('inf')
        n_car = 0
        for i in range(0, len(self.pos)):
            if rh.horiz[i] == False:
                if rh.move_on[i] > self.pos[0] and self.pos[i] <= rh.move_on[0] and self.pos[i] + rh.length[i] - 1 >= rh.move_on[0]:
                    n_car += 1
                    visited = set()
                    visited.add(0)
                    n_car += self.score_state_rec(rh, i, visited)
        return self.estimee1() * 20 + n_car

    def score_state_rec(self, rh, c, visited):
        n_car = 0
        if c not in visited:
            visited.add(c)
            has_2_voisins = self.has_2_voisin(rh, c)
            if has_2_voisins[0]:
                n_car += 4
                n_car += self.score_state_rec(rh, has_2_voisins[1], visited)
                n_car += self.score_state_rec(rh, has_2_voisins[2], visited)
            elif self.has_voisin_backward(rh, c)[0] != self.has_voisin_forward(rh, c)[0]:
                n_car += 1
        return n_car



    # Indique si une voiture à l'index c à deux voisins
    def has_2_voisin(self, rh, c):
        forward = self.has_voisin_forward(rh, c)
        backward = self.has_voisin_backward(rh, c)
        return (forward[0] and backward[0], forward[1], backward[1])

    # Indique si une voiture à l'index c à au moins un voisin
    def has_voisin(self, rh, c):   
        return self.has_voisin_forward(rh, c)[0] or self.has_voisin_backward(rh, c)[0]

    # Indique si une voiture à l'index c à uniquement un seul voisin
    def has_only_1_voisin(self, rh, c):
        return self.has_voisin_backward(rh, c)[0] != self.has_voisin_forward(rh, c)[0]


    # Indique si une voiture à l'index c à un voisin devant
    def has_voisin_forward(self, rh, c):
        for i in range(0, len(self.pos)):
            if i != c and rh.horiz[i] != rh.horiz[c]:
                if rh.move_on[i] == self.pos[c] + rh.length[c]: # Est-ce que t'es sur la colonne/ligne devant
                    if rh.move_on[c] >= self.pos[i] and rh.move_on[c] <= self.pos[i] + rh.length[i] - 1: # Est-ce que tu touches le bloc
                        return (True, i)
        return (False, -1)


    # Indique si une voiture à l'index c à un voisin derrière
    def has_voisin_backward(self, rh, c):    
        for i in range(0, len(self.pos)):
            if i != c and rh.horiz[i] != rh.horiz[c]:
                if rh.move_on[i] == self.pos[c] - 1: # Est-ce que t'es sur la colonne/ligne derriere
                    if rh.move_on[c] >= self.pos[i] and rh.move_on[c] <= self.pos[i] + rh.length[i] - 1: # Est-ce que tu touches le bloc
                        return (True, i)
        return (False, -1)

    def success(self):
        return self.pos[0] == 4
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented

        
        return np.array_equal(self.pos, other.pos)
    
    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37*h + self.pos[i]
        return int(h)
    
    def __lt__(self, other):
        return (self.score) < (other.score)