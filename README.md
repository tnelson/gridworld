# Gridworld project prototyping 

Please put puzzle files in the `puzzles` sub-directory. Each file is a self-contained maze, following this file format:
- The first line contains the number of rows in the grid world. 
- The second line contains the number of columns in the grid world. 
- The third and all other lines each give a single row of the grid world. 
  - The starting location is represented by 'S'.
  - The goal location is represented by '$'. 
  - Squares that cannot be traversed ("mountains") are represented by '#'. 
  - All other squares are represented by the space character (' '). 
  - At the moment, spaces must be added to each line so that the length of each line matches the number of columns declaration. Ideally we would either use a visible character or auto-fill to the column number declared, for ease of use. 

To run, use `python gridworld.py <filename inside the puzzles directory>`.

E.g., 
```
python3 gridworld.py puzzle1.txt
```
