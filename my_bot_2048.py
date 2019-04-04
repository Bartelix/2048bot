'''
page 'http://allthe2048.com/misc/2048-colors.html' open in Chrome on main screen with full mode, scroll down using 6x click
'''

import random, pyautogui, time
import numpy as np
from PIL import ImageGrab, ImageOps

#test_grid = [[4, 64, 8, 8], [64, 2, 0, 2], [16, 4, 0, 0], [4, 2, 2, 0]]
empty_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

cords = [[(586, 272), (700, 266), (820, 265), (936, 259)], [(572, 378), (698, 380), (823, 387), (939, 385)], [(577, 507), (697, 502), (817, 502), (941, 500)], [(577, 626), (699, 629), (819, 627), (942, 623)]]


gray_values = {'empty':195, 2:0, 4:121, 8:136, 16:181, 32:197, 64:178, 128:105, 256:95, 512:60}

l_gray_values = list(gray_values.values())



def game_grid(grid, value_list):
    image = ImageGrab.grab()
    gray_image = ImageOps.grayscale(image)
    #pixels = []
    for row_index in range(4):
        for col_index in range(4):
            pixel = gray_image.getpixel(cords[row_index][col_index])
            #pixels.append(pixel)
            position = value_list.index(pixel)
            if position == 0:
                grid[row_index][col_index] = 0
            else:
                grid[row_index][col_index] = 2 ** position
    #print(pixels)
    return grid


def reverse_grid(grid):
    '''
    Return horizontal reversed input grid
    '''
    new_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for row_index in range(4):
        new_grid[row_index] = grid[row_index][::-1]
    return new_grid


def rotate_90deg(grid):
    '''
    Return rotated input grid about 90deg
    '''
    new_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for row_index in range(4):
        for col_index in range(4):
            new_grid[row_index][col_index] = grid[col_index][- (row_index + 1)]
    return new_grid


def rotate_270deg(grid):
    '''
    Return rotated input grid about -90deg
    '''
    new_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for row_index in range(4):
        for col_index in range(4):
            new_grid[row_index][col_index] = grid[- (col_index + 1)][row_index]
    return new_grid


def move_left(grid):
    '''
    Returns once moved left whole input grid
    '''
    new_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    row_index = 0
    for row in grid:
        prev = -1
        col_index = 0
        for col in row:
            if col != 0:
                if prev == -1:
                    prev = col
                    new_grid[row_index][col_index] = col
                    col_index += 1
                elif prev == col:
                    new_grid[row_index][col_index - 1] = col * 2
                    prev = -1
                else:
                    prev = col
                    new_grid[row_index][col_index] = col
                    col_index += 1
        row_index +=1
    return new_grid


def move_right(grid):
    '''
    Returns once moved right whole input grid
    '''
    return reverse_grid(move_left(reverse_grid(grid)))


def move_up(grid):
    '''
    Returns once moved up whole input grid
    '''
    return rotate_270deg(move_left(rotate_90deg(grid)))


def move_down(grid):
    '''
    Returns once moved down whole input grid
    '''
    return rotate_90deg(move_left(rotate_270deg(grid)))


def calc_weight_grid(grid):
    bordered_grid = [[23, 9, 6.5, 4.5, 3, 2], [6.5, 0, 0, 0, 0, 1,5], [4.4, 0, 0, 0, 0, 1], [2, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    #add grid into bordered_grid
    for row_index in range(4):
        for col_index in range(4):
            bordered_grid[row_index + 1][col_index + 1] = grid[row_index][col_index]

    weight_grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    start_row = 0
    end_row = 3
    for row_index in range(4):
        start_col = 0
        end_col = 3 
        for col_index in range(4):
            suma = 0
            for bd_i in range(start_row, end_row):
                for bd_j in range(start_col, end_col):
                    suma += bordered_grid[bd_i][bd_j]
            start_col += 1
            end_col += 1
            weight_grid[row_index][col_index] = suma / 10
        start_row +=1
        end_row += 1

    return weight_grid


def score_grid(grid):
    '''
    Return calculated value how much score grid have
    '''
    weight_grid = calc_weight_grid(grid)
    score = 0
    it = 0
    for row_index in range(4):
        for col_index in range(4):
            score += grid[row_index][col_index] * weight_grid[row_index][col_index]
            if grid[row_index][col_index] != 0:
                it += 1
    return score / it


random.randint(1,2) * 2 # generate random 2 or 4

def rnd2or4(grid):
    '''
    Add random generated 2 or 4 in random empty place in grid
    '''
    flag = True
    while(flag):
        row_index = random.randint(0, 3)
        col_index = random.randint(0, 3)
        val = random.randint(1,2) * 2
        if grid[row_index][col_index] == 0:
            grid[row_index][col_index] = val
            flag = False
    return grid


def judge(s_left, s_right, s_up, s_down):
    '''
    Return direction which have max average score
    '''
    direction = [['left', 0], ['right', 0], ['up', 0], ['down' ,0]]
    for i in range(4):
        direction[i][1] = eval('np.mean(s_{})'.format(direction[i][0]))
    direction.sort(key = lambda direction: direction[1], reverse = True)
    return direction


def is_move_valid(moved_grid, prev_grid):
    if moved_grid == prev_grid:
        return False
    else:
        return True


def where_to_move(grid):
    '''
    Return direction where bot will move
    '''
    score_left = []
    score_right = []
    score_up = []
    score_down = []
    first_direction = second_direction = third_direction = ['left', 'right', 'up', 'down']
    for i in range(4):
        first_move = eval('move_{}(grid)'.format(first_direction[i]))
        if is_move_valid(first_move, grid):
            first_temp_score = score_grid(first_move) * 0.65
            first_move_rnd = rnd2or4(first_move) 
        else:
            first_temp_score = 0
            first_move_rnd = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        eval('score_{}.append(first_temp_score)'.format(first_direction[i]))
        for j in range(4):
            second_move = eval('move_{}(first_move_rnd)'.format(second_direction[j]))
            if is_move_valid(second_move, first_move_rnd):
                second_temp_score = score_grid(second_move) * 0.25
                second_move_rnd = rnd2or4(second_move)
            else:
                second_temp_score = 0
                second_move_rnd = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            eval('score_{}.append(second_temp_score)'.format(second_direction[j]))
            for k in range(4):
                third_move = eval('move_{}(second_move_rnd)'.format(third_direction[k]))
                if is_move_valid(third_move, second_move_rnd):
                    third_temp_score = score_grid(third_move) * 0.1
                else:
                    third_temp_score = 0
                eval('score_{}.append(third_temp_score)'.format(third_direction[k]))
    move_direction = judge(score_left, score_right, score_up, score_down)
    flag = True
    i = 0
    while flag:
        if not is_move_valid(eval('move_{}(grid)'.format(move_direction[i][0])), grid):
            i += 1
        else:
            return move_direction[i][0]
            flag = False
        

def perform_move(grid):
    pyautogui.press(where_to_move(grid))


def main():
    current_grid = game_grid(empty_grid, l_gray_values)
    print(current_grid)
    perform_move(current_grid)


if __name__ == "__main__":
    time.sleep(3)
    move_nr = 1
    while True:
        main()
        print('move ', move_nr)
        move_nr += 1
        time.sleep(0.3)