# SODUKU
My attempts to crack soduku using Python.

Rule of Soduku:
  https://en.wikipedia.org/wiki/Sudoku

Puzzles extracted from this site: 
  https://sudoku.com/ . 

Puzzles recorded in text files, with each 0 indicating a slot.

I've only applied two strategies: 1. elimination and 2. "unique candidate".
  1. Elimination
     Assign (or update) possible answers (candidates) to each slots, then "confirm" the slots that have only one candidate.
  2. Unique candidate
     Assign (or update) candidates to each slots. If a candidate appears only in one slot along a row, a column OR inside a 3by3 block, then confirm the candidate in that slot.
By iteratively using these two simple strategies, the program can beat easy to hard level Soduku in the mentioned website. However, I've yet to crack the expert level.

I am a newbie to Python, and I deliberately write this program using OOP (well at least I think I am applying OOP) for practice. I am not sure if this is the most efficient/elegant way to solve the problem. 

Thanks for reading this.
