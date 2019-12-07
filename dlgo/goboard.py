##slow_depreciated for zobrist hashing
import copy
from dlgo.gotypes import Player
from dlgo import zobrist

#according to the AGA, on your move you can do 3 actions: play, pass, resign
class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
    
    #places stone
    @classmethod
    def play(cls, point):
        return Move(point=point)

    #passes turn
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    #resigns from game
    @classmethod 
    def resign(cls):
        return Move(is_resign=True)

#creating GoString
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        #changed sets to frozensets. 
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)
    
    #replaces remove_liberties
    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    #replaces add_liberties
    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    #returns a new Go string containing all stones in both strings
    #called when a player places a stone and connects two of its groups.
    def merged_with(self, go_string):
        assert go_string.color == self.color
        #combined stones = self.stones or go_string.stones
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)
    #access the nubmer of liberties at any point
    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

    #Creating board instance, intializing size of board, and grid dict to store strings
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
        #depreciated goboard_slow for this, zobrist 
        self._hash = zobrist.empty_board

    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        #looping through, examining direct neighbors, literally straight out of a DS&A interview question LOL
        for neighbor in point.neighbors():
            #if grid doesnt have anything, go ahead, if it does have something stop. 
            if not self.is_on_grid(neighbor):
                continue
            #if it does have a neighbor, add to grid
            neighbor_string = self._grid.get(neighbor)
            #if there is no string, start one
            if neighbor_string is None:
                liberties.append(neighbor)
            #if there is a string already, and they're the same color, and its not already in the dict, add it to the same color string.
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            #if theres a string already, and the new checked stone is not 
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        #until this line, place_stone remains the same
        new_string = GoString(player, [point], liberties)
         #merge any adjacent strings of the same color
        for same_color_string in adjacent_same_color:  
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        #applying hash code for {point, player}
        self._hash ^= zobrist.hash_code[point, player]  

        #reduce liberties of any adjacent string of opposite color
        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point) 
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            else:
                self._remove_string(other_color_string) 

    #helper method to update grid 
    def _replace_string(self, new_string):
        for point in new_string.stones:
            self._grid[point] = new_string
        
    
    #is on grid,         
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    #returns content of a point on board: returns color if someone's on, or None. 
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    #returns entire string of at a point: GoString if stone is on, or else None
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    #test case for when removing a string creates a liberty. 
    def _remove_string(self, string):
        for point in string.stones:
            #checking if it 
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None
            #zobrist hasing, unapply the hash for this move
            self._hash ^= zobrist.hash_code[point, string.color]
    #return current zobrist hash
    def zobrist_hash(self):
        return self._hash
#encoding game state to know about board position, next player, prev game state, and last move has been played. 
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        #if board is empty, previous states are empty immuitable frozen sets
        if self.previous_state is None:
            self.previous_state = frozenset ()
        #otherwise, augment the states by pair, color of next player and zobrist hash of previous game state.
        else:
            self.previous_states = frozenset(
                previous.previous_state |
            { (previous.next_player, previous.board.zobrist_hash()) } )
        self.last_move = move
    
    #returns gamestate after applying move
    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass
            
    #handling self capture
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0
    
    #handling ko (endless tit-for-tat strategy)
    @property
    #pointer to previous state, enforces ko rule by walking back up tree,
    #and checking the new state against the whole history
    def situation(self):
        return (self.next_player, self.board)

    #once we set up the hashing, this is the main case we're going to speed up, the ko positions.
    def does_move_violate_ko(self,player,move):
        if not move.is_play:
            return False
        #creates a deep copy of board state and have to compare to all
        #previous states.
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        return next_situation in self.previous_states
        #depreciated for loop for zobrist hashing
        
    #wrapping up, making sure each move is valid and not ko or self cap.
    def is_valid_move(self, move):
            if self.is_over():
                return False
            if move.is_pass or move.is_resign:
                return True
            return (
                self.board.get(move.point) is None and 
                not self.is_move_self_capture(self.next_player, move) and 
                not self.does_move_violate_ko(self.next_player, move))
    
    