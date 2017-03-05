import time
from world import World, Cell

SIZE = 50
GENERATIONS = 100
TESTS = 5

def make_world():
    w = World(SIZE, SIZE)

    w.place("1", (2, 2)) \
        .place("1", (2, 3)) \
        .place("1", (2, 4)) \

    return w


def test():
    w = make_world()

    start = 0
    stop = 0

    start = time.time()
    print "Start: " + str(start) + "\n"
    for i in xrange(GENERATIONS):
        w.step()
    stop = time.time()

    print "Stop: " + str(stop) + "\n"

    return stop - start

if __name__ == '__main__':

    results = []
    for i in xrange(TESTS):
        results.append(test())

    avg = sum(results) / TESTS

    out = """
Size: {size}
Generations: {generations}
Tests: {tests}
Max time: {mx}
Min time: {mn}
Avg time: {avg}

""".format(size = SIZE, generations = GENERATIONS, tests = TESTS, mx = max(results), mn = min(results), avg = avg)

    print out
