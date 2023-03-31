# node is anything in a graph you can visit
# edges connect nodes
# weighted edge = certain length/amount

# A* = informed serach, heuristic function, only consider optimal path
# Open set keeps track of nodes you wanna look at next, queue
# add starting node and distance to open set first {(0,A)
# H(n) = distance function, first to end node (guess based on formula)
# H-score^
# G-score = current shortest distance from start node to another node
# F-score = G(n) + H(n)
# comparing the scores to determine which nodes to prioritize
# if you don't know fgh scores, it's infinity

# look at given node, then look at neighbors
# previous scores get updated

import pygame
import math
from queue import PriorityQueue

W = 500
WINDOW = pygame.display.set_mode((W, W))
pygame.display.set_caption('A* pathfinding')

green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)
orange = (255,165,0)
purple = (128,0,128)
gray = (128,128,128)
turquoise = (64,224,208)

class Node:
    # needs to keep track:
    # where it is, its width, neighbors, color
    def __init__(self, r, c, w, tot_row):
        self.r=r
        self.c=c
        self.x=r*w
        self.y=c*w
        self.col=white
        self.neighbors=[]
        self.width = W
        self.tot_rows=tot_row

    def return_position(self):
        return self.r, self.c

    def is_checked(self):
        return self.col==red

    def in_openset(self):
        return self.col==green

    def is_barrier(self):
        return self.col==black

    def is_start(self):
        return self.col==orange

    def is_end(self):
        return self.color==turquoise

    def reset(self):
        self.col=white

    def make_checked(self):
        if self.col != orange and self.col != turquoise:
            self.col=red

    def addto_openset(self):
        if self.col != orange and self.col != turquoise:
            self.col=green

    def make_barrier(self):
        self.col=black

    def make_start(self):
        self.col=orange

    def make_end(self):
        self.col=turquoise

    def create_path(self):
        if self.col != orange and self.col != turquoise:
            self.col=purple

    def create(self,win):
        pygame.draw.rect(win, self.col, (self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        # add to neighbors list all valid squares that can be neighbors
        # neighbors can't be barriers
        self.neighbors=[]
        # down a row
        if self.r < self.tot_rows - 1 and not grid[self.r+1][self.c].is_barrier():
            self.neighbors.append(grid[self.r+1][self.c])

        # up
        if self.r > 0 and not grid[self.r - 1][self.c].is_barrier():
            self.neighbors.append(grid[self.r - 1][self.c])

        # right
        if self.c < self.tot_rows - 1 and not grid[self.r][self.c+1].is_barrier():
            self.neighbors.append(grid[self.r][self.c+1])

        # left
        if self.r > 0 and not grid[self.r][self.c-1].is_barrier():
            self.neighbors.append(grid[self.r][self.c-1])

    def __lt__(self, other): #lt = less than, what happens if 2 nodes are compared
        return False

#heuristic function

def heuristic(point1, point2): #taxicab distance formula
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1-x2) + abs(y1-y2)

def recreate_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.create_path()
        draw()

def algorithm(draw,grid,start,end):
    # can call draw() cuz lambda
    count =0
    open_set=PriorityQueue() # get minimum element
    open_set.put((0,count,start))
    came_from={}
    #g-score
    g = {node: float("inf") for row in grid for node in row}
    g[start]=0
    #f-score
    f = {node: float("inf") for row in grid for node in row}
    f[start] = heuristic(start.return_position(), end.return_position())

    # keeps track of stuff that's in the priority queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        current=open_set.get()[2] # current node we looking at
        open_set_hash.remove(current)

        if current == end:
            recreate_path(came_from,end,draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g = g[current]+1

            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + heuristic(neighbor.return_position(), end.return_position())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.addto_openset()

        draw()
        if current != start:
            current.make_checked()

    return False





def make_grid(rows, width):
    grid = []
    cube_width = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,cube_width,rows)
            grid[i].append(node)

    return grid

def visualize_grid(window,rows,width):
    cube_width= width//rows
    for i in range(rows):
        pygame.draw.line(window,gray,(0, i * cube_width),(width, i * cube_width))
        for j in range(rows):
            pygame.draw.line(window,gray,(j*cube_width,0),(j*cube_width, width))

def draw(window,grid, rows, width):
    window.fill(white)
    for row in grid:
        for node in row:
            node.create(window)

    visualize_grid(window, rows, width)
    pygame.display.update()

def get_clicked_pos(mouse,rows,width):
    gap = width//rows
    y,x = mouse

    r = y//gap
    c = x//gap
    return r,c

def main(window, width):
    rows = 50
    grid= make_grid(rows, width)
    start=None
    end=None

    run = True
    started = False

    while run:
        draw(window, grid, rows, width)
        for event in pygame.event.get(): # check on every event in pygame
            if event.type==pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # if pygame mouse is left clicked
                pos = pygame.mouse.get_pos()
                r,c = get_clicked_pos(pos,rows,width)
                node = grid[r][c]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # right click
                pos = pygame.mouse.get_pos()
                r, c = get_clicked_pos(pos, rows, width)
                node = grid[r][c]
                node.reset()
                if node == start:
                    start = end
                if node == end:
                    end=None

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and start and end:
                    for r in grid:
                        for node in r:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(window,grid,rows,width), grid, start, end)
                    # lambda = unnamed function calling another function

                if event.key == pygame.K_c:
                    start=None
                    end=None
                    grid = make_grid(rows, width)
    pygame.quit()

main(WINDOW,W)


