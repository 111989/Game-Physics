"""
    A* Shortest Path Finding 
    Algorithm implementation 
    and interactive visualization
"""

import pygame
import argparse
from queue import PriorityQueue


class Cell: 
    def __init__(self, cell_row: int, cell_col: int, \
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



def draw(display, display_width: int, display_height: int, \
    matrix, total_cells: int, NONE: tuple):

    # fill display
    display.fill(NONE)

    # draw cells
    for row in matrix:
        for cell in row:
            pygame.draw.rect(display, cell.mode, \
                (cell.cell_row * cell.cell_width , \
                    cell.cell_col * cell.cell_height, \
                        cell.cell_width, cell.cell_height))
                        
    # update display
    pygame.display.update()



def algorithm(display, display_width: int, display_height: int, \
    matrix, total_cells: int, start_cell, end_cell, NONE: tuple, \
        START: tuple, END: tuple, OBSTACLE: tuple, OPEN: tuple, \
            CLOSED: tuple, PATH: tuple):

    def heuristic(cell):
        """
            Returns Manhattan Distance
            between the input cell and end_cell
        """
        x1, y1 = cell.get_cell_position()
        x2, y2 = end_cell.get_cell_position()
        return abs(x2-x1) + abs(y2-y1)


    """ 
        Initialize a Priority Queue 'open_cells'
        for the algorithm to track cells with
        low f-scores, and 'tie_breaker' to break ties 
        between cells with the same f-score.
    """
    tie_breaker = 0 
    start_cell.g_score = 0
    start_cell.f_score = heuristic(start_cell)
    open_cells = PriorityQueue()
    open_cells.put((start_cell.f_score, tie_breaker, start_cell)) 
    open_cells_set = {start_cell} 
    
    

    while not open_cells.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #fetch the cell with the least f_score, call it current_cell
        current_cell = open_cells.get()[2] 
        open_cells_set.remove(current_cell)

        if current_cell == end_cell:
            #draw optimal path
            temp_cell = end_cell
            while temp_cell.parent != start_cell:
                temp_cell = temp_cell.parent
                temp_cell.mode = PATH
                draw(display, display_width, display_height, matrix, total_cells, NONE)
            start_cell.mode, end_cell.mode = START, END
            #optimal path found, terminate algorithm
            break


        #generate successors of the current_cell
        #TOP
        if current_cell.cell_row > 0 and \
            matrix[current_cell.cell_row-1][current_cell.cell_col].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col])
        #RIGHT
        if current_cell.cell_col < current_cell.total_cells-1 and \
            matrix[current_cell.cell_row][current_cell.cell_col+1].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row][current_cell.cell_col+1])
        #BOTTOM
        if current_cell.cell_row < current_cell.total_cells-1 and \
            matrix[current_cell.cell_row+1][current_cell.cell_col].mode != OBSTACLE: 
            current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col])
        #LEFT
        if current_cell.cell_col > 0 and \
            matrix[current_cell.cell_row][current_cell.cell_col-1].mode != OBSTACLE:
            current_cell.successors.append(matrix[current_cell.cell_row][current_cell.cell_col-1])
        # #TOP-LEFT
        # if current_cell.cell_row > 0 and current_cell.cell_col > 0 and \
        #     matrix[current_cell.cell_row-1][current_cell.cell_col-1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col-1])
        # #TOP-RIGHT
        # if current_cell.cell_row > 0 and current_cell.cell_col < current_cell.total_cells-1 and \
        #     matrix[current_cell.cell_row-1][current_cell.cell_col+1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row-1][current_cell.cell_col+1])
        # #BOTTOM-RIGHT
        # if current_cell.cell_row < current_cell.total_cells-1 and current_cell.cell_col < current_cell.total_cells-1 and \
        #     matrix[current_cell.cell_row+1][current_cell.cell_col+1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col+1])
        # #BOTTOM-LEFT
        # if current_cell.cell_row < current_cell.total_cells-1 and current_cell.cell_col > 0 and \
        #     matrix[current_cell.cell_row+1][current_cell.cell_col-1] != OBSTACLE:
        #     current_cell.successors.append(matrix[current_cell.cell_row+1][current_cell.cell_col-1])
        

        min_g_score = current_cell.g_score + 1
        for successor in current_cell.successors:
            if min_g_score < successor.g_score:
                # shorter path to successor found, update successor's attributes
                successor.parent = current_cell
                successor.g_score = min_g_score
                successor.f_score = successor.g_score + heuristic(successor)
                if successor not in open_cells_set:
                    tie_breaker += 1
                    open_cells.put((successor.f_score, tie_breaker, successor))
                    open_cells_set.add(successor)
                    successor.mode = OPEN
                    

        if current_cell != start_cell: 
            current_cell.mode = CLOSED

        draw(display, display_width, display_height, matrix, total_cells, NONE)



def main():
    #initialize cell modes
    NONE = (50, 50, 50) 
    START = (255, 255, 0) 
    END = (0, 255, 255)
    OBSTACLE = (175, 175, 225) 
    OPEN = (255, 200, 200) 
    CLOSED = (255, 128, 128)
    PATH = (128, 225, 0)

    #initialize pygame display
    display = pygame.display.set_mode((display_width, display_height)) 
    pygame.display.set_caption("A* Shortest Path Finding Algorithm")
    
    #generate matrix
    matrix = []
    for cell_row in range(total_cells):
        matrix.append([])
        for cell_col in range(total_cells):
            cell = Cell(cell_row, cell_col, \
                display_width, display_height, total_cells, NONE)
            matrix[cell_row].append(cell)



    start_cell, end_cell = None, None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if pygame.mouse.get_pressed()[0]: #left mouse click
                #get cell position
                cell_width = display_width // total_cells
                cell_height = display_height // total_cells
                cell_row = pygame.mouse.get_pos()[0] // cell_width 
                cell_col = pygame.mouse.get_pos()[1] // cell_height
                cell = matrix[cell_row][cell_col]

                if not start_cell and cell != end_cell: #handling overwrite
                    start_cell = cell
                    start_cell.mode = START
                elif not end_cell and cell != start_cell: #handling overwrite
                    end_cell = cell
                    end_cell.mode = END
                elif cell not in (start_cell, end_cell): #obstacle
                    cell.mode = OBSTACLE


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    algorithm(display, display_width, display_height, matrix, \
                        total_cells, start_cell, end_cell, NONE, START, END, \
                            OBSTACLE, OPEN, CLOSED, PATH)


                
            #update display 
        draw(display, display_width, display_height, matrix, total_cells, NONE)
    pygame.quit()

    

    
if __name__ == '__main__':
    
    #parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type = int, default = 1200, \
        help = 'Display width, must be an integer')
    parser.add_argument('--height', type = int, default = 600, \
        help = 'Display height, must be an integer')
    parser.add_argument('--n', type = int, default = 60, \
        help = 'The display is treated as an (nxn) matrix. \
            Must be an integer that completely divides both width and height')
    
    args = vars(parser.parse_args())
    display_width = int(args['width'])
    display_height = int(args['height'])
    total_cells = int(args['n'])

    
    main()
