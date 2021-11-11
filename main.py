import random
import time


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        if self.parent != None:
            self.g = self.parent.g + 1
        else:
            self.g = 0

    @property
    def h(self):
        """heuristic = 0
        for i in range(1, 8):
            if self.value[i] != i:  # h1: number of misplaced tiles
                heuristic += 1"""
        return manhattan_distance(self.value)  # h2: sum of manhattan distances of misplaced tiles

    @property
    def f(self):
        return self.g + self.h


goal_state = [' ', 1, 2, 3, 4, 5, 6, 7, 8]
closed_list = []  # list of node configurations, used to identify already visited states
possible_moves = ((1, 3), (0, 4, 2), (1, 5), (0, 4, 6),
                  (1, 3, 5, 7), (2, 4, 8), (3, 7),
                  (6, 4, 8), (5, 7))  # possible indices to move to for each index the empty tile could be at


def generate_random_list() -> Node:
    l = [' ', 1, 2, 3, 4, 5, 6, 7, 8]
    l = random.sample(l, len(l))
    return Node(l)


initial_state = generate_random_list()
# initial_state = Node([1, 2, ' ', 3, 4, 5, 6, 7, 8])  # a test configuration
# initial_state = Node([1, 2, 5, 6, 3, 4, ' ', 7, 8])  # a test configuration
# initial_state = Node([' ', 2, 5, 1, 4, 8, 6, 7, 3])  # a test configuration


def generate_moves(node: Node) -> list[(int, Node)]:
    empty_index = node.value.index(' ')
    next_solutions = []

    for i in possible_moves[empty_index]:
        new_node = Node(swap_list_items(node.value, empty_index, i), node)
        if not tuple(new_node.value) in closed_list:  # check if this state was already visited
            next_solutions.append([new_node.f, new_node])

    return next_solutions


def swap_list_items(l: list, p1: int, p2: int) -> list:
    new_list = l.copy()
    new_list[p1], new_list[p2] = new_list[p2], new_list[p1]
    return new_list


def manhattan_distance(l: list) -> int:
    total = 0
    for i in l:
        if i == ' ':
            continue
        position = l.index(i)

        # calculate vertical:
        if i <= 2:
            if position <= 2:
                vertical = 0
            elif position <= 5:
                vertical = 1
            else:
                vertical = 2
        elif i <= 5:
            if 3 <= position <= 5:
                vertical = 0
            else:
                vertical = 1
        else:
            if position <= 2:
                vertical = 2
            elif position <= 5:
                vertical = 1
            else:
                vertical = 0

        # calculate horizontal
        if i % 3 == 0:
            if position % 3 == 0:
                horizontal = 0
            elif position % 3 == 1:
                horizontal = 1
            else:
                horizontal = 2
        elif i % 3 == 1:
            if position % 3 == 1:
                horizontal = 0
            else:
                horizontal = 1
        else:
            if position % 3 == 0:
                horizontal = 2
            elif position % 3 == 1:
                horizontal = 1
            else:
                horizontal = 0
        total += vertical + horizontal
    return total


def display_board(l: list) -> None:
    print(f" {l[0]} | {l[1]} | {l[2]}")
    print(f" {l[3]} | {l[4]} | {l[5]}")
    print(f" {l[6]} | {l[7]} | {l[8]}\n")


def a_star (state: Node) -> list:
    goal_state_appeared = False
    pqueue = []
    while not goal_state_appeared:
        if state.value == goal_state:  # check if it is the goal state
            route_to_goal = [state.value]
            while state.parent != None:
                route_to_goal.append(state.parent.value)
                state = state.parent
            return reversed(route_to_goal)  # reverse the route list as it gets filled from the end

        closed_list.append(tuple(state.value))  # add this node to checked list
        pqueue += generate_moves(state)  # generate children and add it to the list
        pqueue.sort(key=lambda x: x[0])  # sort based on the first element of the 2d list (literally heapify)
        state = pqueue.pop(0)[1]  # pop the first element


print(f'initial board:')
display_board(initial_state.value)
print(f'now finding the route to the solution...)')
print(f'(IF STUCK, TRY AGAIN. SOME RANDOM CONFIGURATIONS INCREASE THE TIME COMPLEXITY BY A CONSIDERABLE AMOUNT)')

t0 = time.perf_counter()
route = a_star(initial_state)
t1 = time.perf_counter()

print(f'\nFOUND!\n\nstarting from the initial state, the route goes like this:')

length = -1
for i in route:
    display_board(i)
    length += 1

print(f'time taken to find: {t1 - t0}s')
print(f'total number of steps needed to solve: {length}')
