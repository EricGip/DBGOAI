# DBGOAI  

The game of Go originated in China in ancient times. It was considered one of the four essential arts of a cultured Chinese scholar in antiquity and is described as a worthy pastime for a gentleman in the Analects of Confucius.

I wanted to take advantage of going to a university with respected professors in multiple disciplines so I decided to take a Game Theory and a mdern Chinese history class as a Statistics major interested in AI.  

From game theory, I wondered how difficult a game of imperfect information can be for AI.  
   - While Go and chess are both sequential, a core strategy for chess is backwards induction since you have perfect information and pieces are fixed. 
   - In Go, you don't have this luxury since you can place a board anywhere on the grid and there are a lot more complicated test cases/strategies you have to account for than you would for chess.   
   
From Chinese history, I understood my ethnic background that i've forgotten and wanted to pay homage to my culture by learning a "worthy past time for a gentleman" rather than the video games that were deemed unworthy by my grandparents. 

I've decided to knock out two birds with one stone by working on a Machine Learning project and learning a game 

Example: Run this in commmand line  
python human_v_bot.py to play vs the bot  
   * To change difficulties, go into the file and change one variable!  
python bot_v_bot.py to watch the bots play  

To do's:  
  for now, we goboard.py is only opitmized with Zobrist hashing but can be much much further optimized. need to create goboard_fast.py
