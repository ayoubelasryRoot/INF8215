from collections import deque
import heapq
import numpy as np
from State import State

class Rushhour:
    
    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz)
        self.horiz = horiz
        self.length = length
        self.move_on = move_on
        self.color = color
        #matrix
        self.free_pos = None
    
    def init_positions(self, state: State):
        self.free_pos = np.ones((6, 6), dtype=bool)
        for i in range(self.nbcars):
            x = self.move_on[i]
            y = state.pos[i]
            if self.horiz[i]:
                self.free_pos[x][y:y + self.length[i]] = False
            else:
                self.free_pos[y: y + self.length[i], x] = False
    
    def possible_moves(self, state: State):
        self.init_positions(state)
        pos_states = []
        # each car we can move is a possible state
        for i in range(self.nbcars):
            x = self.move_on[i]
            y = state.pos[i]         
            if self.horiz[i]:
                # see left part
                k = y - 1
                current_state = state
                while k >= 0:
                    if self.free_pos[x][k] == True:
                        current_state = self.move_left_or_up(i, current_state)
                        pos_states.append(current_state)
                    else:
                        break
                    k -= 1
                # see rigth part
                k = y + self.length[i]
                current_state = state 
                while k < 6:
                    if self.free_pos[x][k] == True:
                        current_state = self.move_rigth_or_down(i, current_state)
                        pos_states.append(current_state)
                    else:
                        break
                    k += 1
            else:
                # see left part
                k = y - 1
                current_state = state
                while k >= 0:
                    if self.free_pos[k][x] == True:
                        current_state = self.move_left_or_up(i, current_state)
                        pos_states.append(current_state)
                    else:
                        break
                    k -= 1
                # see rigth part
                k = y + self.length[i]
                current_state = state 
                while k < 6:
                    if self.free_pos[k][x] == True:
                        current_state = self.move_rigth_or_down(i, current_state)
                        pos_states.append(current_state)
                    else:
                        break
                    k += 1

        return pos_states
    

    def move_left_or_up(self, car_id: int, state: State):
        return state.move(car_id, -1)
    
    def move_rigth_or_down(self, car_id: int, state: State):
        return state.move(car_id, 1)


    def solve(self, state: State):
        return None
    
                    
    def solve_Astar(self, state):
        visited = set()
        visited.add(state)
        
        priority_queue = []
        state.h = state.estimee1()
        heapq.heappush(priority_queue, state)
        
        # TODO
        return None
    
                    
    def print_solution(self, state):
        # TODO
        return 0