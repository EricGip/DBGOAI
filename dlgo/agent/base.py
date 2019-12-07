#this is the interface that all bots will follow

class Agent:
    def __init__(self):
        pass
    
    #selects move in given game state. 
    def select_move(self, game_state):
        raise NotImplementedError()

