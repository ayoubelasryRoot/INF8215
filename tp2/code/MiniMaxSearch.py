class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth
        self.visited = set()

    def minimax_1(self, current_depth, current_state):
        if current_depth == 0:
            score = current_state.score_state(self.rushhour)
            current_state.score = score
            return current_state
        
        pos_moves  = self.rushhour.possible_moves(current_state)
        best_score = float("inf")
        best_move = None
        for state in pos_moves:
            if state not in self.visited:
                child_state = self.minimax_1(current_depth -1, state)
                if child_state.score < best_score:
                    best_score = child_state.score
                    best_move = state
                    current_state.score = child_state.score

        if current_depth == self.search_depth:
            return best_move
        return current_state
        

    
    def minimax_2(self, current_depth, current_state, is_max): 
        if current_depth == 0:
            score = current_state.score_state(self.rushhour)
            current_state.score = score
            return current_state
        
        pos_moves  = None
        if is_max :
            pos_moves = self.rushhour.possible_moves(current_state)
        else:
            pos_moves = self.rushhour.possible_rock_moves(current_state)
        
        best_score = float("inf")
        best_move = None
        for state in pos_moves:
            child_state = self.minimax_2(current_depth -1, state, not is_max)
            if is_max: 
                if state not in self.visited:
                    if child_state.score < best_score:
                        best_score = child_state.score
                        best_move = state
                        current_state.score = child_state.score
            else:
                if child_state.score > best_score:
                    best_score = child_state.score
                    best_move = state
                    current_state.score = child_state.score

        if current_depth == self.search_depth:
            return best_move
        return current_state

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta):
        #TODO
        return best_move

    def expectimax(self, current_depth, current_state, is_max):
        #TODO
        return best_move

    def decide_best_move_1(self): # dispatcher
        if self.state.success() :
            return self.state
        else:
            return self.minimax_1(self.search_depth, self.state)

    def decide_best_move_2(self, is_max):
        if self.state.success() :
            return self.state
        else:
            return self.minimax_2(self.search_depth, self.state, is_max)
    
    def decide_best_move_pruning(self, is_max):
        # TODO
        pass
    
    def decide_best_move_expectimax(self, is_max):
        # TODO
        pass
   
   
    def solve(self, state, is_singleplayer):
        if is_singleplayer:
            self.rushhour.print_pretty_grid(self.state)
            while(not self.state.success()):
                self.state = self.decide_best_move_1()
                self.visited.add(self.state)
                self.print_move(False, self.state)
                x = 0
               # self.rushhour.print_pretty_grid(self.state)
            print('fin apres ' + str(self.state.nb_moves) + " moves")
        else:
            self.rushhour.print_pretty_grid(self.state)
            counter = 0
            while(not self.state.success()):
                is_max = counter % 2 != 0
                self.state = self.decide_best_move_2(is_max)
                self.visited.add(self.state)
                self.print_move(False, self.state)
                x = 0
                counter += 1
               # self.rushhour.print_pretty_grid(self.state)
            print('fin apres ' + str(self.state.nb_moves) + " moves")
        return self.state
    
    def print_move(self, is_max, state):
        string = ""
        if is_max:
            # adversaire
            string = "Roche dans la case : " + str(state.rock[0]) + "-" + str(state.rock[1])
        else:
            # notre ia, qui est trop fort au passage
            string = "Voiture " + self.rushhour.color[state.c] + " vers "
            if self.rushhour.horiz[state.c] == True:
                string += "la "
                if state.d == 1:
                    string += "droite"
                elif state.d == -1:
                    string += "gauche"
            else:
                string += "le "
                if state.d == 1:
                    string += "bas"
                elif state.d == -1:
                    string += "haut"
        print(string)