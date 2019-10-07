import numpy as np
import math
import copy

class State:
    
    """
    Contructeur d'un état initial
    """
    def __init__(self, pos):
        """
        pos donne la position de la voiture i (première case occupée par la voiture);
        """
        self.pos = np.array(pos)
        
        """
        c, d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None
        
        self.nb_moves = 0
        self.h = 0

    """
    Constructeur d'un état à partir mouvement (c,d)
    """
    def move(self, c, d):
        # TODO
        # copy by values
        new_pos = copy.deepcopy(self.pos)
        new_pos[c] = new_pos[c] + d
        new_state = State(new_pos)
        new_state.prev = copy.deepcopy(self)
        new_state.c = c
        new_state.d = d
        new_state.nb_moves = self.nb_moves + 1
        
        return new_state


    """ est il final? """
    def success(self):
        # TODO
        if self.pos[0] >= 4:
            return True
        return False
    

    """
    Estimation du nombre de coup restants 
    """
    
    def estimee1(self):
        return 4 - self.pos[0]


    def estimee2(self, rh):
        carsBetweenExit = 0
        for i in range(1, rh.nbcars):
            if not rh.horiz[i]:
                if rh.move_on[i]  >= self.pos[0] + 2:
                    if rh.length[i] == 2 and (self.pos[i] == 1 or self.pos[i] == 2):
                        carsBetweenExit += 1
                    else :
                        if rh.length[i] == 3 and self.pos[i] <= 2:
                            carsBetweenExit += 1 

        return self.estimee1() + carsBetweenExit
    

    def estimee3(self, rh):
        carsToMove = 0
        for i in range(1, rh.nbcars):
            if not rh.horiz[i]:
                if rh.move_on[i]  > self.pos[0] + 2:
                    if rh.length[i] == 2 and self.pos[i] == 1 or self.pos[i] == 2:
                        carsToMove += 1
                        for j in range (1, rh.nbcars):
                            if rh.horiz[j] and self.pos[i] == 1 and rh.move_on[j] == 0:
                                if self.pos[j] <= rh.move_on[i] and self.pos[j] + rh.length[j] >= rh.move_on[i]:
                                    carsToMove += 1
                            if rh.horiz[j] and self.pos[i] == 1 and rh.move_on[j] == self.pos[i] + rh.length[i]:
                                if self.pos[j] <= rh.move_on[i] and self.pos[j] + rh.length[j] >= rh.move_on[i]:
                                    carsToMove += 1
                    else :
                        if rh.length[i] == 3 and self.pos[i] <= 2:
                            carsToMove += 1
                            for j in range (1, rh.nbcars):
                                if rh.horiz[j] and rh.move_on[j] == 5:
                                    if self.pos[j] <= rh.move_on[i] and self.pos[j] + rh.length[j] >= rh.move_on[i]:
                                        carsToMove += 1 

        return self.estimee1() + carsToMove



    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        if len(self.pos) != len(other.pos):
            print("les états n'ont pas le même nombre de voitures")
        
        return np.array_equal(self.pos, other.pos)
        
    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37*h + self.pos[i]
        return int(h)
    
    def __lt__(self, other):
        return (self.nb_moves + self.h) < (other.nb_moves + other.h)
