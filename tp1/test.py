from collections import deque
import heapq
import numpy as np
from State import State
import queue


class Rushhour:

    def __init__(self, horiz, length, move_on, color=None):
        self.nbcars = len(horiz)
        self.horiz = horiz
        self.length = length
        self.move_on = move_on
        self.color = color
        # matrix
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
            state_left = state
            state_rigth = state
            # left pointer move left or up
            left_pointer = state.pos[i] - 1
            # right pointer move rigth or down
            rigth_pointer = state.pos[i] + self.length[i]
            # here we check when we move left or up
            while left_pointer != -1 or rigth_pointer != 6:
                if left_pointer >= 0:
                    is_place_free = self.free_pos[x][left_pointer] if self.horiz[i] else self.free_pos[left_pointer][x]
                    if is_place_free:
                        state_left = self.move_left_or_up(i, state_left)
                        pos_states.append(state_left)
                        left_pointer -= 1
                    else:
                        left_pointer = -1
                else:
                    left_pointer = -1
                # here we check when we move dow or rigth
                if rigth_pointer < 6:
                    is_place_free = self.free_pos[x][rigth_pointer] if self.horiz[i] else self.free_pos[rigth_pointer][x]
                    if is_place_free:
                        state_rigth = self.move_rigth_or_down(i, state_rigth)
                        pos_states.append(state_rigth)
                        rigth_pointer += 1
                    else:
                        rigth_pointer = 6
                else:
                    rigth_pointer = 6

        return pos_states

    def move_left_or_up(self, car_id: int, state: State):
        return state.move(car_id, -1)

    def move_rigth_or_down(self, car_id: int, state: State):
        return state.move(car_id, 1)

    def solve(self, state: State):
        done = False
        priority_states = queue.Queue()
        priority_states.put(state)
        visted_states = {}
        while not done:
            current: State = priority_states.get()
            if current.success():
                return current
            next_moves = self.possible_moves(current)
            for next_state in next_moves:
                state_code = next_state.__hash__()
                if state_code not in visted_states:
                    priority_states.put(next_state)
                    visted_states[state_code] = 1
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
        steps = []
        current_state = state
        while current_state.prev is not None:
            car = 0
            for i in range(6):
                move = ""
                if current_state.pos[i] != current_state.prev.pos[i]:
                    car = i
                    if current_state.pos[i] > current_state.prev.pos[i]:
                        if self.horiz[i] == True:
                            move = "droite"
                        else:
                            move = "bas"
                    elif current_state.pos[i] < current_state.prev.pos[i]:
                        if self.horiz[i] == True:
                            move = "gauche"
                        else:
                            move = "haut"
                    break
            steps.append(
                ("Voiture {} vers la {}".format(self.color[car], move)))
            current_state = current_state.prev
        k = 0
        for i in reversed(range(len(steps))):
            k += 1
            print("{}. {}".format(k, steps[i]))
