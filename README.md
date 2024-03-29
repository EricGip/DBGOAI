# DBGOAI  

Step 1: represent Go board in Python and state legal moves.
Step 2: 

Example: Run this in commmand line  
---------------
python human_v_bot.py to play vs the bot  
   * To change difficulties, go into the file and change one variable!  
python bot_v_bot.py to watch the bots play  

To do's
--------------
  for now, we goboard.py is only opitmized with Zobrist hashing but can be much much further optimized. need to create goboard_fast.py

Background
------------------
The game of Go originated in China in ancient times. It was considered one of the four essential arts of a cultured Chinese scholar in antiquity and is described as a worthy pastime for a gentleman in the Analects of Confucius.

I wanted to take advantage of going to a university with respected professors in multiple disciplines so I decided to take a Game Theory and a modern Chinese history class as a Statistics major interested in AI to gain as much domain knowledge as possible.. 


From game theory, I wondered how difficult a game of imperfect information can be for AI.  
   - While Go and chess are both sequential, a core strategy for chess is backwards induction since you have perfect information and pieces are fixed. 
   - In Go, you don't have this luxury since you can place a board anywhere on the grid/pieces are not fixed and there are a lot more complicated test cases/strategies you have to account for than you would for chess, allowing me to be more prepared for realistic cases with TensorFlow. 
       - After the first two moves of a Chess game, there are 400 possible next moves. In Go, there are close to 130,000, so our neural network can be much more unique than other Go bots.  
       - E.g Territory to speed up games, Ko, Self Capture, Eyes.

I've decided to knock out two birds with one stone by working on a Machine Learning project and deeper understanding for strategy games.
   * Games also simplify complexities of real life, so we only need to focus on the algorithm.

Sources
----------
Pumperla, M., & Ferguson, K. (2019). Deep learning and the game of Go. Shelter Island, NY: Manning Publications Co.
