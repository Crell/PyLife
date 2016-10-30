
import copy


# @todo Make organism and Rock a subclass of Thing, or something, so that Cells don't need to be regenerated and can just hold a Thing.

class Cell:
    neighbors = []

    occupant = None

    def __init__(self, occupant = None):
        self.occupant = occupant or Occupant()

    def isAlive(self):
        return self.occupant.isAlive()

    def setOccupant(self, occupant):
        self.occupant = occupant

    def setSourceNeighbors(self, cells):
        self.neighbors = cells

    def updateValue(self):
        numLiving = len([n for n in self.neighbors if n.isAlive()])
        # Each cell with one or no neighbors dies, as if by solitude.
        # Each cell with four or more neighbors dies, as if by overpopulation.
        # Each cell with two or three neighbors survives.

        self.occupant.setAlive((numLiving == 3) or (numLiving == 2 and self.isAlive()))

    def __str__(self):
        return str(self.occupant)


class Occupant:
    def isAlive(self):
        return False

    def setAlive(self, living): pass

    def __str__(self):
        return 'A' if self.isAlive() else 'D'


class Organism(Occupant):
    living = False

    def __init__(self, live=True):
        self.living = live

    def isAlive(self):
        return self.living

    def setAlive(self, living):
        self.living = living


class Rock(Occupant):

    def __str__(self):
        return 'R'


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

        self.setGridSourceNeighbors(self.grid[0], self.grid[1])
        self.setGridSourceNeighbors(self.grid[1], self.grid[0])

    def setGridSourceNeighbors(self, grid, target):
        for (x, y), cell, in grid.iteritems():
            cell.setSourceNeighbors(self.getCellNeighbors(target, x, y))

    def getCellNeighbors(self, target, x, y):
        x_range = range(max(x-1, 0), min(x+1, self.rows-1)+1)
        y_range = range(max(y-1, 0), min(y+1, self.cols-1)+1)

        #print x, max(x-1, 0), min(x+1, self.rows)+1, x_range

        neighbors = [target[(i, j)]
                     for i in x_range
                     for j in y_range
                     if not (i == x and j == y)]
        return neighbors

    def activeGrid(self):
        return self.grid[self.current]

    def cellAt(self, x, y):
        active = self.activeGrid()
        return active[(x, y)].occupant

    def placeRock(self, x, y):
        cell = self.activeGrid()[(x, y)]
        cell.setOccupant(Rock())
        return self

    def placeOrganism(self, x, y, org = None):
        org = org or Organism()
        self.activeGrid()[(x, y)].setOccupant(org)
        return self

    def step(self):
        nextCurrent = (self.current + 1) % 2
        nextGrid = self.grid[nextCurrent]
        # @todo Turn this into a map call if possible.
        for coord, cell in nextGrid.iteritems():
            cell.updateValue()

        self.current = nextCurrent
        return

    def newgrid(self, rows, cols):
        grid = {}
        # @todo There is probably a comprehension version of this.
        for r in range(0, rows):
            for c in range(0, cols):
                grid[(r, c)] = Cell()
        return grid

    def __str__(self):
        grid = self.activeGrid()
        out = 'On grid ' + str(self.current) + ':\n'
        for x in range(self.rows):
            for y in range(self.cols):
                out += str(grid[(x, y)])
            out += '\n'
        return out

if __name__ == '__main__':

    w = World(3, 3)

    assert len(w.getCellNeighbors(w.grid[1], 0, 0)) == 3

    #print w.grid[0][(1, 1)].occupant
    assert isinstance(w.grid[0][(1, 1)].occupant, Occupant)

    w = World(5, 10)
    w.placeOrganism(2, 2).placeOrganism(2, 3).placeOrganism(2, 4)

    print w
    w.step()
    print w

