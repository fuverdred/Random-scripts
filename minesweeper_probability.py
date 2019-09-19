from random import shuffle

X = 30 # Grid width
Y = 16 # Grid height

coverage = 0.20625 # Fraction that are mines
num_mines = int(X*Y*coverage)

coords = [(i, j) for i in range(Y) for j in range(X)] # every coord on grid

def make_grid():
    grid = [[0 for _ in range(X)] for _ in range(Y)]
    shuffle(coords)
    for i, j in coords[:num_mines]:
        grid[i][j] = 1
    return grid

def count_mines(grid, x, y):
    surrounding = [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1)
                   if not i==j==0]
    for i,j in surrounding:
        if not grid[i][j]:
            break # break as soon as an adjacent square is not a mine
    else:
        return 1
    return 0

def check_grid(grid):
    eight_count = 0
    for i, j in coords[num_mines:]: #  only iterate over non-mines
        if i in (0,Y-1) or j in (0,X-1): # boundary case
            continue
        eight_count += count_mines(grid, i, j)
    return eight_count
        
def crunch_the_numbers(repeats=1E6):
    eight_count = 0
    repeats = int(repeats)
    for i in range(repeats):
        if i != 0 and i%1E5 == 0:
            print(f'{i} minesweeper grids checked\n'
                  f'{eight_count} eight squares found')
        grid = make_grid()
        eight_count += check_grid(grid)
    #probability that 8 squares are mines, fractional coverage^8, given
    #that the current square is not a mine (1-fractional coverage)
    probability_val = coverage**8 * (1-coverage)
    #Exclude edge squares, which cannot be surrounded by mines
    crunched_val = eight_count / (repeats * (X-2) * (Y-2))
    print(f'Theoretical value: {probability_val}\n'
          f'Found value: {crunched_val}')

if __name__ == '__main__':
    crunch_the_numbers()
