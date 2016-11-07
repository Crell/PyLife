import unittest
import pytest

import world


# Cell tests

@pytest.mark.parametrize("start,neighbors,expected",  [
    # Empty, 1 neighbor
    ('E', [world.Cell('1')], 'E'),
    ('E', [world.Cell('E')], 'E'),
    # Empty, 2 neighbors
    ('E', [world.Cell('E'), world.Cell('1')], 'E'),
    ('E', [world.Cell('1'), world.Cell('1')], 'E'),
    # Empty, 3 neighbors
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('1')], '1'),
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('F')], '1'),
    # Empty, 4 neighbors
    ('E', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('E')], '1'), # Born from 3 neighbors
    ('E', [world.Cell('1'), world.Cell('2'), world.Cell('1'), world.Cell('R')], 'E'), # Hostile neighbor prevents birth
    # Living, 1 neighbor
    ('1', [world.Cell('1')], 'E'),
    # Living, 2 neighbors
    ('1', [world.Cell('1'), world.Cell('1')], '1'),
    ('1', [world.Cell('1'), world.Cell('F')], '1'),
    # Living, 3 neighbors
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1')], '1'),
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('F')], '1'),
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('2')], '1'), # Still 2 friendly neighbors
    # Living, 4 neighbors
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('1')], 'E'), # Die from over-population
    ('1', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('F')], '1'), # Food doesn't cause over-population
    # Rocks should always stay a rock
    ('R', [], 'R'),
    ('R', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('R')], 'R'),
    # Food should always stay food
    ('F', [], 'F'),
    ('F', [world.Cell('1'), world.Cell('1'), world.Cell('1'), world.Cell('R')], 'F'),
])
def test_update_value(start, neighbors, expected):
        # The state of the local cell doesn't matter, it's the mirror cell that matters.
        c = world.Cell(start, world.Cell(start))

        c.set_source_neighbors(neighbors)
        c.update_value()

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

    assert w.cell_at((2, 3)).state == 'R'
    assert w.cell_at((1, 1)).state == 'R'
    assert w.cell_at((4, 9)).state == 'R'
    assert w.cell_at((4, 4)).state == 'E'


def test_populate_organisms():
    w = world.World(5, 10)
    w.place('1', (2, 3)) \
        .place('1', (4, 9))

    assert w.cell_at((2, 3)).state == '1'
    assert w.cell_at((1, 1)).state == 'E'
    assert w.cell_at((4, 9)).state == '1'


def test_get_cell_neighbors():
    w = world.World(3, 3)
    assert len(w.get_cell_neighbors(w.grid[1], (0, 0))) == 3
    assert len(w.get_cell_neighbors(w.grid[1], (0, 1))) == 5
    assert len(w.get_cell_neighbors(w.grid[1], (0, 2))) == 3
    assert len(w.get_cell_neighbors(w.grid[1], (1, 0))) == 5
    assert len(w.get_cell_neighbors(w.grid[1], (1, 1))) == 8
    assert len(w.get_cell_neighbors(w.grid[1], (1, 2))) == 5
    assert len(w.get_cell_neighbors(w.grid[1], (2, 0))) == 3
    assert len(w.get_cell_neighbors(w.grid[1], (2, 1))) == 5
    assert len(w.get_cell_neighbors(w.grid[1], (2, 2))) == 3


def test_step():
    w = world.World(5, 10)
    w.place('1', (2, 2)) \
        .place('1', (2, 3)) \
        .place('1', (2, 4))
    w.step()

    # Two cells should have died
    assert w.cell_at((2, 2)).state == 'E'
    assert w.cell_at((2, 4)).state == 'E'

    # One cell doesn't change
    assert w.cell_at((2, 3)).state == '1'

    # Two cells should be born
    assert w.cell_at((1, 3)).state == '1'
    assert w.cell_at((3, 3)).state == '1'


def test_step_with_food_and_rocks():
    w = world.World(5, 10)
    w.place('1', (2, 2)) \
        .place('F', (2, 3)) \
        .place('1', (2, 4)) \
        .place('R', (3, 3))
    w.step()

    # Two cells should have died.
    assert w.cell_at((2, 2)).state == 'E'
    assert w.cell_at((2, 4)).state == 'E'

    # Food cell doesn't change.
    assert w.cell_at((2, 3)).state == 'F'

    # Rock cell doesn't change.
    assert w.cell_at((3, 3)).state == 'R'

    # One cell should be born.
    assert w.cell_at((1, 3)).state == '1'


def test_step_multiplayer():
    w = world.World(5, 10)
    w.place('1', (2, 2)) \
        .place('2', (2, 3)) \
        .place('1', (2, 4))
    w.step()

    print w

    # Because they're different species, everyone should have died.
    assert w.cell_at((2, 2)).state == 'E'
    assert w.cell_at((2, 4)).state == 'E'
    assert w.cell_at((2, 3)).state == 'E'

    # No one should be born.
    assert w.cell_at((1, 3)).state == 'E'
    assert w.cell_at((3, 3)).state == 'E'



if __name__ == '__main__':
    unittest.main()
