from RushHour import Rushhour
from State import State
from MiniMaxSearch import MiniMaxSearch

def test_print_move():
    rh = Rushhour([True], [2], [2], ["rouge"])
    s = State([0])
    s = s.put_rock((3,1)) # Roche dans la case 3-1
    s = s.move(0, 1) # Voiture rouge vers la droite

    algo = MiniMaxSearch(rh, s, 1)
    algo.print_move(True, s)
    algo.print_move(False, s)

test_print_move()


rh = Rushhour([True, False, False, False, True],
                 [2, 3, 2, 3, 3],
                 [2, 4, 5, 1, 5],
                 ["rouge", "vert", "bleu", "orange", "jaune"])
s = State([1, 0, 1, 3, 2])
algo = MiniMaxSearch(rh, s, 4) 
algo.rushhour.init_positions(s)
print(algo.rushhour.free_pos)
algo.solve(s, False)