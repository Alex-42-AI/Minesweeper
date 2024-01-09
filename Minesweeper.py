from random import randint
from os import system, name
def print_grid():
    for i in range(rows):
        print('|', end='')
        for ii in range(cols):
            print(current_grid[i][ii], end=' ')
        print('|', i)
    print(' ', end='')
    for ii in range(cols):
        print(ii, end=' ')
    print()
def guess(r, c):
    if current_grid[r][c] == ' ':
        current_grid[r][c] = str(field[r][c])
    if not field[r][c]:
        zeros = []
        checked.append((r, c))
        for i in range(r - 1, r + 2):
            for ii in range(c - 1, c + 2):
                if 0 <= i < rows and 0 <= ii < cols and (i, ii) not in checked:
                    current_grid[i][ii] = str(field[i][ii])
                    if zeros and not field[i][ii]:
                        zeros.append((i, ii))
                    elif not field[i][ii]:
                        zeros = [(i, ii)]
        for pair in zeros:
            guess(pair[0], pair[1])
def expand(r, c):
    total_discovered_mines = 0
    total_empty_squares = 0
    for i in range(r - 1, r + 2):
        for ii in range(c - 1, c + 2):
            if 0 <= i < rows and 0 <= ii < cols:
                total_discovered_mines += current_grid[i][ii] == 'F'
                total_empty_squares += current_grid[i][ii] == ' '
    if total_discovered_mines == field[r][c]:
        for i in range(r - 1, r + 2):
            for ii in range(c - 1, c + 2):
                if 0 <= i < rows and 0 <= ii < cols:
                    if not field[i][ii]:
                        guess(i, ii)
                    if str(field[i][ii]) == "True":
                        if current_grid[i][ii] == ' ':
                            lost.append(1)
                            return
                    else:
                        current_grid[i][ii] = str(field[i][ii])
    elif field[r][c] == total_empty_squares + total_discovered_mines:
        for i in range(r - 1, r + 2):
            for ii in range(c - 1, c + 2):
                if 0 <= i < rows and 0 <= ii < cols:
                    if isinstance(field[i][ii], bool):
                        current_grid[i][ii] = 'F'
def loose():
    clear()
    print('Game over!')
    for i in range(rows):
        for ii in range(cols):
            if current_grid[i][ii] == 'F':
                if isinstance(field[i][ii], bool):
                    current_grid[i][ii] = 'M'
                else:
                    current_grid[i][ii] = '!'
            elif current_grid[i][ii] == ' ':
                if isinstance(field[i][ii], bool):
                    current_grid[i][ii] = 'M'
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
while True:
    rows, cols = list(map(int, input().split(maxsplit=2)))
    mines = 2 * rows * cols // 7
    total_mines = mines
    field = [[] for i in range(rows)]
    for i in range(rows):
        for _ in range(cols):
            field[i].append(0)
    while mines:
        for i in range(rows):
            for j in range(cols):
                if mines:
                    field[i][j] = int(randint(0, 1) and randint(0, 1))
                    if field[i][j]:
                        field[i][j] = True
                        mines -= 1
    extra_grid = [[field[i][j] for j in range(cols)] for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if not extra_grid[i][j]:
                for curr_row in range(i - 1, i + 2):
                    for curr_col in range(j - 1, j + 2):
                        if 0 <= curr_row < rows and 0 <= curr_col < cols:
                            field[i][j] += extra_grid[curr_row][curr_col]
    current_grid = [[' ' for _ in range(cols)] for i in range(rows)]
    # for i in range(rows):
    #     print(' '.join(str(j) for j in field[i]))
    holder = True
    flags = 0
    while holder:
        clear()
        print(total_mines - flags)
        print_grid()
        row, col, action = list(input().split(maxsplit=3))
        row, col = abs(int(row)), abs(int(col))
        if not (0 <= row < rows and 0 <= col < cols) or action.lower() not in ['step', 'mark', 'unmark']:
            continue
        if isinstance(field[row][col], bool) and action == 'step':
            loose()
            break
        if total_mines - flags:
            if action == 'mark' and current_grid[row][col] == ' ':
                flags += 1
                current_grid[row][col] = 'F'
        if action == 'step':
            if current_grid[row][col] == ' ':
                checked = []
                guess(row, col)
            else:
                lost = []
                expand(row, col)
                if lost:
                    loose()
        elif action == 'unmark' and current_grid[row][col] == 'F':
            flags -= 1
            current_grid[row][col] = ' '
        holder = False
        for i in range(rows):
            for j in range(cols):
                if current_grid[i][j] == ' ':
                    holder = True
                    break
            if holder:
                break
    print_grid()
    a = input('Press enter to continue...')
