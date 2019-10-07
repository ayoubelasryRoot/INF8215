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
            y = state.pos[i]
            state_left = state
            state_rigth = state
            left_pointer = y - 1
            rigth_pointer = y + self.length[i]
            # the main idea is when we check left vs right is the same operation as down vs up
            while left_pointer != -1 or rigth_pointer != 6:
                new_x, new_y = self.x_y_from_horz(self.horiz[i], x, left_pointer)
                if left_pointer >= 0 and self.free_pos[new_x][new_y]:
                    state_left = self.move_left_or_up(i, state_left)
                    pos_states.append(state_left)
                    left_pointer -= 1
                else:
                    left_pointer = -1
                new_x, new_y = self.x_y_from_horz(self.horiz[i], x, rigth_pointer)
                if rigth_pointer < 6 and self.free_pos[new_x][new_y]:
                    state_rigth = self.move_rigth_or_down(i, state_rigth)
                    pos_states.append(state_rigth)
                    rigth_pointer += 1
                else:
                    rigth_pointer = 6
        return pos_states

    def x_y_from_horz(self, horz, x, y):
        # if you're not in horizontal mode we need to inverse x and y
        x_prime = x
        y_prime = y
        if not horz:
            x_prime = y
            y_prime = x
        return x_prime, y_prime

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
        done = False
        visited = set()
        visited.add(state)

        priority_queue = []
        heapq.heappush(priority_queue, state)

        while not done:
            current: State = heapq.heappop(priority_queue)
            if current.success():
                return current
            next_moves = self.possible_moves(current)
            for next_state in next_moves:
                if next_state not in visited:
                    next_state.h = next_state.estimee1()
                    visited.add(next_state)
                    heapq.heappush(priority_queue, next_state)
        return None

    def print_solution(self, state):
        steps = []
        current_state = state
        car = 0
        while current_state.prev is not None:
            vec_change = current_state.pos - current_state.prev.pos
            pos_changed = np.nonzero(np.absolute(vec_change) == 1)[0]
            if len(pos_changed) > 0:
                car = pos_changed[0]
                if vec_change[car] > 0:
                    move = "la droite" if self.horiz[car] else "le bas"
                elif vec_change[car] < 0:
                    move = "la gauche" if self.horiz[car] else "le haut"
            steps.append(("Voiture {} vers {}".format(self.color[car], move)))
            current_state = current_state.prev
        k = 0
        for step in reversed(steps):
            k += 1
            print("{}. {}".format(k, step))
