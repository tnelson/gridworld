
def puzzle(puzzle_file):
    '''Run the puzzle with the given specification file.'''
    # Read in a puzzle specification from a file. Note that this is a relative path. 
    # If run from within VSCode, VSCode may be looking relative to whatever folder it has been
    # "opened" on. As a workaround, you can re-open in this folder, or just use the terminal directly.
    # Likewise, some operating systems will require us to say which encoding is being used. I add it
    # here for completeness, although it's potentially a bit confusing. 
    puzzle_file = open(f'puzzles/{puzzle_file}', 'r', encoding='utf8')
    # Get the number of columns for convenience, and the number of rows for checking against what we read in.
    num_rows = int(puzzle_file.readline())
    num_columns = int(puzzle_file.readline())
    # Read all _remaining_ lines. Each one corresponds to a row in the gridworld. 
    # Start with empty gridworld, no rows.
    world: list[list[str]] = []

    # Note well: at the moment, the puzzle file needs blank space filling out the lines to equal length!
    for line in puzzle_file.readlines():
        row = [marker for marker in line if marker != '\n'] # don't keep newlines
        # Check that the appropriate number of columns is present
        if(len(row) != num_columns):
            raise ValueError(f'Each row needed to be {num_columns} marks long; got: {row}')
        # Check that the marks are only those we know how to deal with
        if(any([True for mark in row if mark not in ['#', '$', 'S', ' ']])):
            raise ValueError(f'Each row needed to contain only the marks: # (mountain), $ (goal), S (start), or space (empty). Got: {row}')
        # Add this row to the gridworld
        world.append(row)

    if(len(world) != num_rows):
        raise ValueError(f'Expect {num_rows}; got: {len(world)} rows.')

    # Find the starting and goal locations, which had better be unique. 
    # Use list comprehension to _filter_ the cell indexes, keeping only those with matching contents.
    # Note: if you forget to use == instead of = (assignment) Python gives an unhelpful error message. :-(
    starts = [(r, c) for r in range(len(world)) for c in range(len(world[r])) if world[r][c] == 'S']
    goals  = [(r, c) for r in range(len(world)) for c in range(len(world[r])) if world[r][c] == '$']
    if(len(starts) != 1):
        raise ValueError(f'Needed only one (S)tarting location; got {len(starts)} of them.')
    if(len(goals) != 1):
        raise ValueError(f'Needed only one goal ($) location; got {len(goals)} of them.')

    # Start the recursive search! Right now, the only "to do" location is where we currently are.
    # We'll also remember that we've been in that place, so we don't loop back later.
    return search([starts[0]], goals[0], [starts[0]], world, num_rows, num_columns, {})

def NORTH(loc): return (loc[0]-1,loc[1])
def SOUTH(loc): return (loc[0]+1,loc[1])
def WEST(loc):  return (loc[0],loc[1]-1)
def EAST(loc):  return (loc[0],loc[1]+1)

def search(todo, goal, visited, world, num_rows, num_columns, parents): 
    '''Search for the `goal`, starting from the `current_location`. Avoid already `visited` locations.'''
    
    # If we have nothing to visit, stop! 
    if len(todo) < 1: 
        print("Nothing remaining to visit; not found.")
        return None
    # Otherwise, see if we can move anywhere from this location
    current_location = todo[0] 
    todo = todo[1:] # remove the first location in the to-do queue
    
    print("-----------------------------------")
    print("World:")
    show(current_location, goal, world, num_rows, num_columns)
    
    # Are we done searching? 
    if current_location == goal:
        print("Found!")
        # Start the process of rebuilding the path we took to get here.
        return [goal]
    
    # What are our options for moving from here?
    options = [NORTH(current_location), SOUTH(current_location), WEST(current_location), EAST(current_location)]
    # Which of the options are actually valid? 
    options = [(x,y) for x,y in options 
               if (x >= 0 and y >= 0 and x < num_rows and y < num_columns and 
                   world[x][y] != '#' and (x,y) not in visited)]
    print(f'At {current_location}; movement options: {options}. Remaining queue: {todo}')
    print(f'Parents map: {parents}')
    
    if len(options) < 1: 
        print("Nowhere new to move from here. Continuing with the todo list of locations to explore...")
    
    # Explore all the options, breadth-first, by adding them to the queue (and remembering how we 
    # first got to them, which will help us re-assemble the shortest path). 
    new_visited = visited + options
    new_todo = todo + options
    # We first discovered each option from the current location. Remember this permanently; this is the 
    # way we optimally find the goal.
    parents.update({option: current_location for option in options})
    
    results = search(new_todo, goal, new_visited, world, num_rows, num_columns, parents)
    if results == None: 
        return None 
    else: 
        # We found the goal, so let's walk back up the recursion stack and reassemble the path we used to find it.
        #print(f'Found; results[0]={results[0]}, current={current_location}; parents={parents.keys()}')
        if current_location == parents[results[0]]:
            # Productive path; remember.
            print(f'Extending path to go via {current_location}: {[current_location] + results }.')
            return [current_location] + results 
        else: 
            print(f'{current_location} was not used. Backtracking and returning {results}...')
            return results

def show(current_location, goal, world, num_rows, num_columns): 
    for row in range(num_rows):
        rowstr = ''
        for col in range(num_columns):
            if (row,col) == current_location: 
                rowstr += "*"
            elif world[row][col] == ' ':
                rowstr += "_" # for readability
            else: 
                rowstr += world[row][col]
        print(rowstr)

if __name__ == '__main__':
    # The `argv` variable will give all arguments to the program received at the terminal.
    # The first argument is the name of the Python file, so we ignore it.
    from sys import argv
    if(len(argv) != 2): 
        raise ValueError(f'Please enter a single puzzle filename (within the `puzzles` folder) as an argument.')
    print(puzzle(argv[1]))


