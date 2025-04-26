import numpy as np
import bisect
from PIL import Image

def add_g(x, y, lim=None, base=2):
    cc = 0
    g = x.copy()
    def add_rec(cs):
        nonlocal cc
        toDo = cs.copy()
        toDo.sort(key = lambda c: -c[0]-c[1])
        while toDo:
            coord = toDo.pop()
            cc += 1
            if not lim or (coord[0] <= lim and coord[1] <= lim):
                #print(coord)
                if g[coord] >= base or g[coord] < 0:
                    # adjacent stuff
                    cx = (coord[0] + 1, coord[1])
                    cy = (coord[0], coord[1] + 1)
                    # carry
                    d = g[coord] // base
                    g[coord] = g[coord] % base
                    g[cx] = d + g.get(cx, 0)
                    g[cy] = d + g.get(cy, 0)
                    # recurse
                    if cx not in toDo:
                        #toDo.append(cx)
                        bisect.insort(toDo, cx, key=lambda c: -c[0]-c[1])
                    if cy not in toDo:
                        bisect.insort(toDo, cy, key=lambda c: -c[0]-c[1])
                        #toDo.append(cy)
                    #toDo.sort(key = lambda c: -c[0]-c[1])
            elif coord in g:
                g.pop(coord)
    # addition elementwise
    for tile in y:
        g[tile] = g.get(tile, 0) + y.get(tile)
    # carry
    add_rec(list(g.keys()))
    print(cc)
    return g

def print_g_manual(g, width, height):
    for i in range(height):
        for j in range(width):
            um = g.get((i,j), 0)
            print((" " if um == 0 else "#"), end=" ")
        print()
    print()

def print_g(g):
    width = 1
    height = 1
    for tile in g:
        if tile[1] > width:
            width = tile[1]
        if tile[0] > height:
            height = tile[0]
    print_g_manual(g, width, height)

def print_im(g):
    width = 1
    height = 1
    for tile in g:
        if tile[1] > width:
            width = tile[1]
        if tile[0] > height:
            height = tile[0]
    image = Image.new(mode = "RGB", size=(width,height), color="white")
    pm = image.load()
    for i in range(height):
        for j in range(width):
            um = g.get((i,j), 0)
            if um == 1:
                pm[i, j] = (0, 0, 0)
            if um == 2:
                pm[i, j] = (255, 0, 0)
            if um == 3:
                pm[i, j] = (255, 255, 0)
    image.show()
    # image.save("output.png", format="png")

"""
grid = dict()
grid[(0,0)] = 1
for i in range(25):
    print(i)
    grid = add_g(grid, grid, lim=512)
"""

"""
# 2**25
grid = dict()
grid[(0,0)] = 2**25
grid = add_g(grid, {(0,0):0}, lim=4096)
print_im(grid)
"""

"""
# - 1/3
grid = dict()
grid[(0,0)] = sum(4 ** n for n in range(128))
grid = add_g(grid, {(0,0):0}, lim=128)
print_im(grid)
g2 = add_g(grid, grid, lim=128)
print_im(g2)
g3 = add_g(g2, grid, lim=128)
print_im(g3)
"""

# 1/3
grid = dict()
grid[(0,0)] = 1 + sum((-2) ** n for n in range(1025))
grid = add_g(grid, {(0,0):0}, lim=512)
print_im(grid)


"""
# 1/4 base 3
grid = dict()
grid[(0,0)] = sum((-3) ** n for n in range(1024))
grid = add_g(grid, {(0,0):0}, lim=512, base=3)
print_im(grid)
"""

"""
grid = dict()
grid[(0,0)] = -3**40
grid = add_g(grid, {(0,0):0}, lim=64, base=3)
print_im(grid)
"""
"""
grid = dict()
grid[(0,0)] = -2**10
grid = add_g(grid, {(0,0):0}, lim = 100)
print_im(grid)
"""
"""
grid = dict()
grid[(0,0)] = 2**10
grid = add_g(grid, {(0,0):0}, lim = 100)
print_im(grid)
"""
"""
grid = dict()
for i in range(30):
    grid[(i, 29 - i)] = (1) ** i
grid = add_g({(0,0):0}, grid, lim = 100)
print_im(grid)
"""
             
#print_g(grid)
#image = Image.new(mode = "RGB", size=(400,400), color="white")
#image.show()
#image.save("output", format="png")

