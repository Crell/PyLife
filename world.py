
import copy

"""
Needed refactor notes:

Occupants:
- Food
- Rock
- Empty (Changeable)
- Friend (Changeable)
- Enemy (Changeable)

Living cell survives if:
(friends + enemies) < 4
friends+food >=2

Cell is born if:
friends + food = 3



addSpecies(1, Species())
place(s, 2, 3)

addType('R', Rock())
addType('F', Food())
addType('0', Empty())
addType('1', Organism())
addType('2', Organism())
place('R', 2, 4)

if occupant.changeable:
    if organism:
        neighbors = getNeighbors
        friends = neighbors if same ID
        enemies = neighbors if same type, different ID
        if (friends+enemies < 4 and friends+food >=2):
            change to empty
    if empty:
        neighbors = getNeighbors
        if (neighbors of same species or food) = 3 and neighbors < 4
            change to species X


"""

class Cell:
    neighbors = []

    occupant = None
    mirrorCell = None

    def __init__(self, occupant = None, mirror = None):
        # Default to a dead organism
        self.occupant = occupant or Organism(False)
        self.mirrorCell = mirror

    def isAlive(self):
        return self.occupant.isAlive()

    def setOccupant(self, occupant):
        self.occupant = occupant

    def setMirrorCell(self, cell):
        self.mirrorCell = cell

    def setSourceNeighbors(self, cells):
        self.neighbors = cells

    def updateValue(self):
        numLiving = len([n for n in self.neighbors if n.isAlive()])

        # Each cell with one or no neighbors dies, as if by solitude.
        # Each cell with four or more neighbors dies, as if by overpopulation.
        # Each cell with two or three neighbors survives.

        self.occupant.setAlive((numLiving == 3) or (numLiving == 2 and self.mirrorCell.isAlive()))

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

        self.setGridMirrors(self.grid[0], self.grid[1])
        self.setGridMirrors(self.grid[1], self.grid[0])

    def setGridMirrors(self, source, target):
        for (x, y), cell, in source.iteritems():
            cell.setMirrorCell(target[(x, y)])

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
            #print coord, "Before: " + str(cell)
            cell.updateValue()
            #print coord, "After: " + str(cell)

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
        # out = ''
        # for idx, g in self.grid.iteritems():
        #     out += 'On grid ' + str(idx) + ':\n'
        #     for x in range(self.rows):
        #         for y in range(self.cols):
        #             out += str(g[(x, y)])
        #     out += '\n'
        # return out

        grid = self.activeGrid()
        out =''
        out += 'On grid ' + str(self.current) + ':\n'
        for x in range(self.rows):
            for y in range(self.cols):
                out += str(grid[(x, y)])
            out += '\n'
        return out

if __name__ == '__main__':

    w = World(3, 3)
    w.placeOrganism(0, 1).placeOrganism(1, 1).placeOrganism(2, 1)

    print w
    w.step()
    print w
    w.step()
    print w
    w.step()
    print w
    w.step()
    print w

