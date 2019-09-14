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
        new_pos = copy.deepcopy(self.pos)
        new_pos[c] = new_pos[c] + d
        new_state = State(new_pos)
        new_state.prev = copy.deepcopy(self)
        new_state.c = c
        new_state.d = d
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
        # TODO
        return 0

    def estimee2(self, rh):
        # TODO
        return 0
    
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
