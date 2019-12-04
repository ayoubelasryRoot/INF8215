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
                    blocking_cars.append(i)
        return blocking_cars

    def score_state(self, rh):
        previous_move_car = self.c
        previous_move_direction = self.d

        if self.prev.c == self.c and self.d == -1 * self.prev.d:
            return 100
        
        blocking_cars = self.get_blocking_cars(rh, self)
        if previous_move_car == 0:
            if previous_move_direction == 1:
                return -1
            else:
                return 15
        
        score = 0.5

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
        
        if rh.horiz[self.c] == True :
            if self.d == -1:
                if self.prev.pos[self.c] + rh.length[self.c] > self.pos[0] + 2:
                    return -1
            else:
                return 0.5

        prev_blocking_cars = self.get_blocking_cars(rh, self.prev)
        if len(blocking_cars) < len(prev_blocking_cars):
            return -10
        elif len(blocking_cars) > len(prev_blocking_cars):
            return 20
        return score

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