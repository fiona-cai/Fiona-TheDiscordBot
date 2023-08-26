def list_unique(l):
    nums = []
    for num in l:
        if num != 0:
            if num in nums:
                return False
            else:
                nums.append(num)
    return True


def valid_row(sudoku, row_idx):
    row = sudoku[row_idx]
    return list_unique(row)


def valid_col(sudoku, col_idx):
    col = []
    for i in range(9):
        col.append(sudoku[i][col_idx])
    return list_unique(col)


def valid_square(sudoku, square_nr):
    square = []

    square_x, square_y = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)][square_nr]

    for y in range(square_y * 3, square_y * 3 + 3):
        for x in range(square_x * 3, square_x * 3 + 3):
            square.append(sudoku[y][x])
    return list_unique(square)


def print_matrix(sudoku, predefined, ans):
    for x, row in enumerate(sudoku):
        for y, val in enumerate(row):
            if (y + 1) % 3:
                ans += ('{:2} '.format(val))
            else:
                ans += ('{:2}  '.format(val))

        if (x + 1) % 3:
            ans += ('\n')
        else:
            ans += ('\n\n')
    return ans


def increase_x(x, y):
    x += 1
    if x > 8:
        x = 0
        y += 1
    return x, y


def decrease_x(x, y):
    x -= 1
    if x < 0:
        x = 8
        y -= 1
    return x, y

def generate_sudoku(sudoku):
    ans = ""
    predefined = [[False for i in range(9)] for j in range(9)]
    for x in range(9):
        for y in range(9):
            if sudoku[y][x] != 0:
                predefined[y][x] = True

    try_nr = [[1 for k in range(9)] for l in range(9)]
    current_x = 0
    current_y = 0

    while predefined[current_y][current_x]:
        current_x, current_y = increase_x(current_x, current_y)
        if current_y > 8:
            ans += ("Sudoku seems to be solved already...\n")
            ans = (print_matrix(sudoku, predefined, ans))
            return ans

    while True:
        sudoku[current_y][current_x] = try_nr[current_y][current_x]

        valid = True
        for i in range(9):
            valid = valid and valid_row(sudoku, i) and valid_col(sudoku, i) and valid_square(sudoku, i)

        if valid:
            current_x, current_y = increase_x(current_x, current_y)
            if current_y > 8:
                ans += ("Solution\n")
                ans = (print_matrix(sudoku, predefined, ans))
                
                return ans
            while predefined[current_y][current_x]:
                current_x, current_y = increase_x(current_x, current_y)
                if current_y > 8:
                    ans += ("Solution\n")
                    ans = (print_matrix(sudoku, predefined, ans))
                    return ans
        else:
            while True:
                if try_nr[current_y][current_x] == 9:
                    try_nr[current_y][current_x] = 1
                    sudoku[current_y][current_x] = 0
                    current_x, current_y = decrease_x(current_x, current_y)
                    if current_y < 0:
                        ans += ("Not Solvable\n")
                        ans = (print_matrix(sudoku, predefined, ans))
                        return ans
                    while predefined[current_y][current_x]:
                        current_x, current_y = decrease_x(current_x, current_y)
                        if current_y < 0:
                            ans += ("Not Solvable\n")
                            ans = (print_matrix(sudoku, predefined, ans))
                            return ans
                else:
                    try_nr[current_y][current_x] += 1
                    break