
import copy

class Cell:
    def isAlive(self):
        return False

class Organism(Cell):
    living = False

    def __init__(self, live=True):
        self.living = live

    def isAlive(self):
        return self.living

class Rock(Cell): pass


class World:

    grid = dict()
    current = 0
    rows = 0
    cols = 0

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        grid = self.newgrid(rows, cols)

        self.grid[0] = copy.deepcopy(grid)
        self.grid[1] = copy.deepcopy(grid)

    def activeGrid(self):
        return self.grid[self.current]

    def cellAt(self, x, y):
        active = self.activeGrid()
        return active[(x, y)]

    def placeRock(self, x, y):
        self.activeGrid()[(x, y)] = Rock()
        return self

    def placeOrganism(self, x, y, org = Organism()):
        self.activeGrid()[(x, y)] = org
        return self

    def newgrid(self, rows, cols):
        grid = {}
        # @todo There is probably a comprehension version of this.
        for r in range(0, rows):
            for c in range(0, cols):
                grid[(r, c)] = Organism()
        return grid

        # @todo But it's not this.
        #self.grid = {r for r in range(rows) for c in range(cols)}
        #self.grid[1] = {r for r in range(rows) for c in range(cols)}
        #print self.grid


if __name__ == '__main__':
    w = World(2, 3)

    #print w.grid



