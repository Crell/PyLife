import unittest
import pytest

import world


# Cell tests


@pytest.mark.parametrize("start,neighbors,expected",  [
    ('E', [world.Cell('1')], 'E'),
    ('E', [world.Cell('E')], 'E'),
    ('E', [world.Cell('E'), world.Cell('1')], 'E'),
    ('E', [world.Cell('E'), world.Cell('1')], 'E'),
    ('E', [world.Cell('1'), world.Cell('1')], 'E'),
    ('E', [world.Cell('1'), world.Cell('1')], 'E'),
    ('1', [world.Cell('1'), world.Cell('1')], '1'),
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('1')], '1'),
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('F')], '1'),
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('E')], '1'),
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('1')], 'E'),
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('F')], '1'),
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('R')], '1'),
])
def test_update_value(start, neighbors, expected):
        # The state of the local cell doesn't matter, it's the mirror cell that matters.
        c = world.Cell('E', world.Cell(start))

        c.setSourceNeighbors(neighbors)
        c.updateValue()

        assert expected == c.state


# World tests

def test_create_world():
    w = world.World(5, 10)
    assert isinstance(w.grid, dict)
    assert isinstance(w.grid[0], dict)
    assert isinstance(w.grid[1], dict)
    assert isinstance(w.grid[0][(1, 1)], world.Cell)
    assert w.grid[0][(1, 1)].state == 'E'


def test_populate_rocks():
    w = world.World(5, 10)

    w.place('R', (2, 3))
    w.place('R', (2, 3)) \
        .place('R', (1, 1)) \
        .place('R', (4, 9))

    assert w.cellAt((2, 3)).state == 'R'
    assert w.cellAt((1, 1)).state == 'R'
    assert w.cellAt((4, 9)).state == 'R'
    assert w.cellAt((4, 4)).state == 'E'


def test_populate_organisms():
    w = world.World(5, 10)
    w.place('1', (2, 3)) \
        .place('1', (4, 9))

    assert w.cellAt((2, 3)).state == '1'
    assert w.cellAt((1, 1)).state == 'E'
    assert w.cellAt((4, 9)).state == '1'


def test_get_cell_neighbors():
    w = world.World(3, 3)
    assert len(w.getCellNeighbors(w.grid[1], (0, 0))) == 3
    assert len(w.getCellNeighbors(w.grid[1], (0, 1))) == 5
    assert len(w.getCellNeighbors(w.grid[1], (0, 2))) == 3
    assert len(w.getCellNeighbors(w.grid[1], (1, 0))) == 5
    assert len(w.getCellNeighbors(w.grid[1], (1, 1))) == 8
    assert len(w.getCellNeighbors(w.grid[1], (1, 2))) == 5
    assert len(w.getCellNeighbors(w.grid[1], (2, 0))) == 3
    assert len(w.getCellNeighbors(w.grid[1], (2, 1))) == 5
    assert len(w.getCellNeighbors(w.grid[1], (2, 2))) == 3


def test_step():
    w = world.World(5, 10)
    w.place('1', (2, 2)) \
        .place('1', (2, 3)) \
        .place('1', (2, 4))
    w.step()

    # Two cells should have died
    assert w.cellAt((2, 2)).state == 'E'
    assert w.cellAt((2, 4)).state == 'E'

    # One cell doesn't change
    assert w.cellAt((2, 3)).state == '1'

    # Two cells should be born
    assert w.cellAt((1, 3)).state == '1'
    assert w.cellAt((3, 3)).state == '1'


"""

def test_step_with_rocks():
    w = world.World(5, 10)

    w.place('1', (2, 2)) \
        .place('1', (2, 3)) \
        .place('1', (2, 4)) \
        .place('R', (4, 7))


    w.step()

    assert isinstance(w.cellAt((4, 7)), world.Rock)
"""

if __name__ == '__main__':
    unittest.main()
