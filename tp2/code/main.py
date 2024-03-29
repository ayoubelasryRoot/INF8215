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

# test_print_move()


# rh = Rushhour([True, False, False, False, True],
#                  [2, 3, 2, 3, 3],
#                  [2, 4, 5, 1, 5],
#                  ["rouge", "vert", "bleu", "orange", "jaune"])
# s = State([1, 0, 1, 3, 2])
# algo = MiniMaxSearch(rh, s, 4) 
# algo.rushhour.init_positions(s)
# print(algo.rushhour.free_pos)
# algo.solve(s, True)


rh = Rushhour([True, False, False, False, True],
                 [2, 3, 2, 3, 3],
                 [2, 4, 5, 1, 5],
                 ["rouge", "vert", "bleu", "orange", "jaune"])
s = State([1, 0, 1, 3, 2])
algo = MiniMaxSearch(rh, s, 1) 
algo.rushhour.init_positions(s)
print(algo.rushhour.free_pos)
algo.solve(s, True)


# # solution optimale: 16 moves
# rh = Rushhour([True, True, False, False, True, True, False, False],
#                  [2, 2, 3, 2, 3, 2, 3, 3],
#                  [2, 0, 0, 0, 5, 4, 5, 3],
#                  ["rouge", "vert", "mauve", "orange", "emeraude", "lime", "jaune", "bleu"])
# s = State([1, 0, 1, 4, 2, 4, 0, 1])
# algo = MiniMaxSearch(rh, s, 1) 
# algo.rushhour.init_positions(s)
# print(algo.rushhour.free_pos)
# algo.solve(s, True) 

# rh = Rushhour([True, False, True, False, False, False, True, True, False, True, True],
#                  [2, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2],
#                  [2, 0, 0, 3, 4, 5, 3, 5, 2, 5, 4],
#                  ["rouge", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
# s = State([0, 0, 3, 1, 2, 1, 0, 0, 4, 3, 4])
# algo = MiniMaxSearch(rh, s,1)
# algo.rushhour.init_positions(s)
# print(algo.rushhour.free_pos)
# algo.solve(s, True)