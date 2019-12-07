#we can now run a really basic game in the command line, we're going to use our by typing in 'python bot_v_bot.py' in the command line.
from dlgo import agent
from dlgo import goboard_slow
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import  time

def main():
    board_size = 9
    game = goboard_slow.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.naive.RandomBot(),
        gotypes.Player.white: agent.naive.RandomBot(),
    }
    while not game.is_over():
        #set timer for bot moves so you can actually see whats going on
        time.sleep(0.3)
        #before each move, clear the screen so we can always print to the same position on the command line.
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()