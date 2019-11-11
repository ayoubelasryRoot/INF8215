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
        s.prev = self.prev
        s.nb_moves = self.nb_moves
        s.c = self.c 
        s.d = self.d
        s.rock = rock_pos
        return s
            
    def estimee1(self):
        # TODO
        caseFinal = 4 # 6 cases - 2 de longueurs
        return  caseFinal - self.pos[0]

    
    def get_blocking_cars(self, rh, state):
        blocking_cars = []
        # voiture critiques previous state
        for i in range(1, rh.nbcars):
            is_car_vertical =  not rh.horiz[i]
            if is_car_vertical and rh.move_on[i]  > state.pos[0] + 1:
                # check if car of size 2 is blocking
                is_car_2_block = rh.length[i] == 2 and (state.pos[i] == 1 or state.pos[i] == 2)
                is_car_3_block = rh.length[i] == 3 and state.pos[i] <= 2
                if is_car_2_block or is_car_3_block:
                    color = rh.color[i]
                    blocking_cars.append(i)
        return blocking_cars

    def score_state(self, rh):
        previous_state = self.prev
        previous_move_car = self.c
        previous_move_direction = self.d
        color = rh.color[previous_move_car]

        if self.prev.c == self.c and self.d == -1 * self.prev.d:
            return 100
        
        blocking_cars = self.get_blocking_cars(rh, self)
        if previous_move_car == 0:
            if previous_move_direction == 1:
                return -1
            else:
                return 15
        
        score = 0

        if previous_move_car in blocking_cars:
            if rh.length[previous_move_car] == 3:
                if previous_move_direction == -1:
                    score += 0.5
                else:
                    nb_blocking = 0
                    col = rh.move_on[previous_move_car]
                    start_row = self.pos[previous_move_car] + 2
                    for i in range(start_row, 6):
                        if rh.free_pos[i][col] == False:
                            nb_blocking += 1
                    if nb_blocking == 0:
                        score -= 0.5
                    else:
                        score += nb_blocking
            
            else:
                if previous_move_direction == -1:
                    nb_blocking = 0
                    free = 0
                    col = rh.move_on[previous_move_car]
                    for i in reversed(range(self.pos[previous_move_car])):
                        if rh.free_pos[i][col] == False:
                            nb_blocking += 0.5
                        else:
                            free += 1
                    
                    if nb_blocking == 0:
                        score -= 0.5*2
                    else:
                        score += nb_blocking

                else:
                    nb_blocking = 0
                    col = rh.move_on[previous_move_car]
                    for i in range(self.pos[previous_move_car] + 1, 5):
                        if rh.free_pos[i][col] == False:
                            nb_blocking += 0.5
                    if nb_blocking == 0:
                        score -= 0.5
                    else:
                        score += nb_blocking
        
        if self.d == -1 and rh.horiz[self.c] == True and self.pos[self.c] <= rh.move_on[]

        prev_blocking_cars = self.get_blocking_cars(rh, self.prev)
        if len(blocking_cars) < len(prev_blocking_cars):
            return -10
        elif len(blocking_cars) > len(prev_blocking_cars):
            return 20
        # if len(prev_blocking_cars) > len(blocking_cars):
        #     return -1
        return score


        # row = rh.move_on[previous_move_car]
        # col = self.pos[previous_move_car]
        # if rh.horiz[previous_move_car] is True :
        #     test = previous_move_direction * -1 + col
        #     if 
    
    # def unlock_block_car(car_id, blocking_cars, rh):
    #     for blocking_car in blocking_cars:
    #         if rh.length[blocking_car] == 3:
                          
        # # graphe de dependance
        # linked_cars = []
        # for car_index in blocking_cars:
        #     linked_list = []
        #     position = previous_state.pos[car_index]
        #     if rh.length[car_index] == 3:
        #         blocking_cars = []

        #         for i in range(1, rh.nbcars):
        #             if (rh.horiz[i] 
        #                 and rh.move_on[i] >= position + 3 
        #                 and previous_state.pos[i] <= rh.move_on[car_index]
        #                 and previous_state.pos[i] + rh.length[i] >= rh.move_on[car_index]):
        #                 blocking_cars.append(i)
                
        #         for i in range(position + 3, 6):
        #             if not rh.free_pos[i][rh.move_on[car_index]]:
        #                 occupied_col.append(i)
                
        #     linked_cars.append(linked_list)
        # # calucler son score
                
        

    # # TODO
    # carsToMove = 0
    # self.score = 50 * self.pos[0] + (-10 * self.nb_moves)
    # for i in range(1, rh.nbcars):
    #     if not rh.horiz[i] and rh.move_on[i]  > self.pos[0] + 2:
    #             if rh.length[i] == 2 and self.pos[i] == 1 or self.pos[i] == 2:
    #                 self.score -= 60
    #                 for j in range (1, rh.nbcars):
    #                     if rh.horiz[j] and (rh.move_on[j] < self.pos[i] or (rh.move_on[j] > self.pos[i] + rh.length[i] and rh.move_on[j] < 5)):
    #                         if self.pos[j] <= rh.move_on[i] and self.pos[j] + rh.length[j] >= rh.move_on[i]:
    #                             self.score -= 30
    #                             if not rh.free_pos[rh.move_on[j], self.pos[j]]:
    #                                 self.score -= 20
    #             else :
    #                 if rh.length[i] == 3 and self.pos[i] <= 2:
    #                     self.score -= 60
    #                     for j in range (1, rh.nbcars):
    #                         if rh.horiz[j] and rh.move_on[j] >= 3:
    #                             if self.pos[j] <= rh.move_on[i] and self.pos[j] + rh.length[j] >= rh.move_on[i]:
    #                                 self.score -=75
    #                                 if not rh.free_pos[rh.move_on[j], self.pos[j] - 1]:
    #                                     self.score -= 20
                                    
                                    

    # return self.score
        

    # def score_state(self, rh):
    #     if self.prev != None and self.c == self.prev.c and self.prev.d == self.d * -1:
    #         return float('inf')
    #     n_car = 0
    #     for i in range(0, len(self.pos)):
    #         if rh.horiz[i] == False:
    #             if rh.move_on[i] > self.pos[0] and self.pos[i] <= rh.move_on[0] and self.pos[i] + rh.length[i] - 1 >= rh.move_on[0]:
    #                 n_car += 1
    #                 visited = set()
    #                 visited.add(0)
    #                 n_car += self.score_state_rec(rh, i, visited)
    #     return self.estimee1() * 20 + n_car

    # def score_state_rec(self, rh, c, visited):
    #     n_car = 0
    #     if c not in visited:
    #         visited.add(c)
    #         has_2_voisins = self.has_2_voisin(rh, c)
    #         if has_2_voisins[0]:
    #             n_car += 4
    #             n_car += self.score_state_rec(rh, has_2_voisins[1], visited)
    #             n_car += self.score_state_rec(rh, has_2_voisins[2], visited)
    #         elif self.has_voisin_backward(rh, c)[0] != self.has_voisin_forward(rh, c)[0]:
    #             n_car += 1
    #     return n_car



    # # Indique si une voiture à l'index c à deux voisins
    # def has_2_voisin(self, rh, c):
    #     forward = self.has_voisin_forward(rh, c)
    #     backward = self.has_voisin_backward(rh, c)
    #     return (forward[0] and backward[0], forward[1], backward[1])

    # # Indique si une voiture à l'index c à au moins un voisin
    # def has_voisin(self, rh, c):   
    #     return self.has_voisin_forward(rh, c)[0] or self.has_voisin_backward(rh, c)[0]

    # # Indique si une voiture à l'index c à uniquement un seul voisin
    # def has_only_1_voisin(self, rh, c):
    #     return self.has_voisin_backward(rh, c)[0] != self.has_voisin_forward(rh, c)[0]


    # # Indique si une voiture à l'index c à un voisin devant
    # def has_voisin_forward(self, rh, c):
    #     for i in range(0, len(self.pos)):
    #         if i != c and rh.horiz[i] != rh.horiz[c]:
    #             if rh.move_on[i] == self.pos[c] + rh.length[c]: # Est-ce que t'es sur la colonne/ligne devant
    #                 if rh.move_on[c] >= self.pos[i] and rh.move_on[c] <= self.pos[i] + rh.length[i] - 1: # Est-ce que tu touches le bloc
    #                     return (True, i)
    #     return (False, -1)


    # # Indique si une voiture à l'index c à un voisin derrière
    # def has_voisin_backward(self, rh, c):    
    #     for i in range(0, len(self.pos)):
    #         if i != c and rh.horiz[i] != rh.horiz[c]:
    #             if rh.move_on[i] == self.pos[c] - 1: # Est-ce que t'es sur la colonne/ligne derriere
    #                 if rh.move_on[c] >= self.pos[i] and rh.move_on[c] <= self.pos[i] + rh.length[i] - 1: # Est-ce que tu touches le bloc
    #                     return (True, i)
    #     return (False, -1)

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