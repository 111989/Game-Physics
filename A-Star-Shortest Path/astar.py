""" A* Shortest Path Finding Algorithm implementation 
    and interactive visualization """

import pygame
import argparse
from heapq import heappush, heappop

class Cell: 
    def __init__(self, cell_row: int, cell_col: int, 
        display_width: int, display_height: int, total_cells: int, NONE: tuple):
        
        self.cell_row = cell_row
        self.cell_col = cell_col
        self.total_cells = total_cells
        self.cell_width = display_width // self.total_cells
        self.cell_height = display_height // self.total_cells
        self.mode = NONE
        self.parent = None
        self.successors = []
        self.g_score = float('inf')
        self.f_score = float('inf')

    def get_cell_position(self):
        return self.cell_row, self.cell_col

    def __lt__(self, other):
        return False



# fill display
# draw cells
# update display
def draw(display, display_width: int, display_height: int, 
    matrix, total_cells: int, NONE: tuple):
    
    display.fill(NONE)
    for row in matrix:
        for cell in row:
            pygame.draw.rect(display, cell.mode, 
                (cell.cell_row * cell.cell_width , 
                    cell.cell_col * cell.cell_height, 
                        cell.cell_width, cell.cell_height))
    pygame.display.update()



# Initializes a Priority Queue called 'open_cells'
# for the algorithm to track cells with low f-scores, 
# and 'tie_breaker' to break ties between cells with 
# the same f-score.
def algorithm(display, display_width: int, display_height: int, matrix, 
        total_cells: int, start_cell, end_cell, NONE: tuple, START: tuple, 
            END: tuple, OBSTACLE: tuple, OPEN: tuple, CLOSED: tuple, PATH: tuple):

    # Returns Manhattan Distance between the input cell and end_cell
    def heuristic(cell):
        
        x1, y1 = cell.get_cell_position()
        x2, y2 = end_cell.get_cell_position()
        return abs(x2-x1) + abs(y2-y1)

    tie_breaker = 0 
    start_cell.g_score = 0
    start_cell.f_score = heuristic(start_cell)
    open_cells = [(start_cell.f_score, tie_breaker, start_cell)]
    open_cells_set = {start_cell} 

    # Fetch the cell with the least f_score, call it current_cell.
    # If current_cell == end_cell, optimal path is found, draw it 
    # and terminate algorithm. Else, generate successors (neighbours)
    # of the current_cell and update the attributes of a successor 
    # when a shorter path to it is found.
    while open_cells:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cell = heappop(open_cells)[2] 
        open_cells_set.remove(current_cell)

        if current_cell == end_cell:
            temp_cell = end_cell
            while temp_cell.parent != start_cell:
                temp_cell = temp_cell.parent
                temp_cell.mode = PATH
                draw(display, display_width, display_height, matrix, total_cells, NONE)
            start_cell.mode, end_cell.mode = START, END
            break

        # TOP
        if current_cell.cell_row > 0 and \
            matrix[current_cell.cell_row-1][current_cell.cell_col].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col])
        # RIGHT
        if current_cell.cell_col < current_cell.total_cells-1 and \
            matrix[current_cell.cell_row][current_cell.cell_col+1].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row][current_cell.cell_col+1])
        # BOTTOM
        if current_cell.cell_row < current_cell.total_cells-1 and \
            matrix[current_cell.cell_row+1][current_cell.cell_col].mode != OBSTACLE: 
            current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col])
        # LEFT
        if current_cell.cell_col > 0 and \
            matrix[current_cell.cell_row][current_cell.cell_col-1].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row][current_cell.cell_col-1])
        # # TOP-LEFT
        # if current_cell.cell_row > 0 and current_cell.cell_col > 0 and \
        #     matrix[current_cell.cell_row-1][current_cell.cell_col-1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col-1])
        # # TOP-RIGHT
        # if current_cell.cell_row > 0 and current_cell.cell_col < current_cell.total_cells-1 and \
        #     matrix[current_cell.cell_row-1][current_cell.cell_col+1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col+1])
        # # BOTTOM-RIGHT
        # if current_cell.cell_row < current_cell.total_cells-1 and current_cell.cell_col < current_cell.total_cells-1 and \
        #     matrix[current_cell.cell_row+1][current_cell.cell_col+1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col+1])
        # # BOTTOM-LEFT
        # if current_cell.cell_row < current_cell.total_cells-1 and current_cell.cell_col > 0 and \
        #     matrix[current_cell.cell_row+1][current_cell.cell_col-1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col-1])
        
        min_g_score = current_cell.g_score + 1
        for successor in current_cell.successors:
            if min_g_score < successor.g_score:
                successor.parent = current_cell
                successor.g_score = min_g_score
                successor.f_score = successor.g_score + heuristic(successor)
                if successor not in open_cells_set:
                    tie_breaker += 1
                    heappush(open_cells, (successor.f_score, tie_breaker, successor))
                    open_cells_set.add(successor)
                    successor.mode = OPEN
                    
        if current_cell != start_cell: 
            current_cell.mode = CLOSED

        draw(display, display_width, display_height, matrix, total_cells, NONE)



def main():

    # initialize cell modes
    # initialize pygame display
    # generate matrix
    NONE = (50, 50, 50) 
    START = (255, 255, 0) 
    END = (0, 255, 255)
    OBSTACLE = (175, 175, 225) 
    OPEN = (255, 200, 200) 
    CLOSED = (255, 128, 128)
    PATH = (128, 225, 0)

    display = pygame.display.set_mode((display_width, display_height)) 
    pygame.display.set_caption("A* Shortest Path Finding Algorithm")

    matrix = []
    for cell_row in range(total_cells):
        matrix.append([])
        for cell_col in range(total_cells):
            cell = Cell(cell_row, cell_col, display_width, display_height, total_cells, NONE)
            matrix[cell_row].append(cell)

    # run
    start_cell, end_cell = None, None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            # On left mouse click, get the position of 
            # the cell and initialize/ set cell modes.
            if pygame.mouse.get_pressed()[0]: 
                cell_width = display_width // total_cells
                cell_height = display_height // total_cells
                cell_row = pygame.mouse.get_pos()[0] // cell_width 
                cell_col = pygame.mouse.get_pos()[1] // cell_height
                cell = matrix[cell_row][cell_col]

                if not start_cell and cell != end_cell: 
                    start_cell = cell
                    start_cell.mode = START
                elif not end_cell and cell != start_cell: 
                    end_cell = cell
                    end_cell.mode = END
                elif cell not in (start_cell, end_cell): 
                    cell.mode = OBSTACLE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    algorithm(display, display_width, display_height, matrix, total_cells, 
                        start_cell, end_cell, NONE, START, END, OBSTACLE, OPEN, CLOSED, PATH)

        #update display 
        draw(display, display_width, display_height, matrix, total_cells, NONE)

    pygame.quit()

    
    
if __name__ == '__main__':
    
    #parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type = int, default = 1200, help = 'Display width, must be an integer')
    parser.add_argument('--height', type = int, default = 600, help = 'Display height, must be an integer')
    parser.add_argument('--n', type = int, default = 60, help = 'The display is treated as an (nxn) matrix. Must be an integer that completely divides both width and height')
    
    args = vars(parser.parse_args())
    display_width = int(args['width'])
    display_height = int(args['height'])
    total_cells = int(args['n'])

    main()
