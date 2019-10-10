#!/usr/bin/python3

# tanglenum - enumeration of planar Tangles
# Copyright 2019 Douglas A. Torrance

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import networkx as nx

def tuple_add(v, w):
    return(v[0] + w[0], v[1] + w[1])

def tuple_subtract(v, w):
    return(v[0] - w[0], v[1] - w[1])


class PolystickEdge:
    def __init__(self, vertices):
        self.vertices = sorted(vertices)
        # tail is the left or bottom vertex
        self.tail = self.vertices[0]
        # head is the right or top vertex
        self.head = self.vertices[1]

    def __eq__(self, other):
        return self.vertices == other.vertices

    def __hash__(self):
        return 0

    def __repr__(self):
        return str(self.vertices)

    def is_horizontal(self):
        return tuple_subtract(self.head, self.tail) == (1, 0)

    def is_vertical(self):
        return tuple_subtract(self.head, self.tail) == (0, 1)

    def neighbors(self):
        if self.is_horizontal():
            return [
                PolystickEdge([self.tail, tuple_add(self.tail, (0, 1))]),
                PolystickEdge([self.tail, tuple_add(self.tail, (-1, 0))]),
                PolystickEdge([self.tail, tuple_add(self.tail, (0, -1))]),
                PolystickEdge([self.head, tuple_add(self.head, (0, 1))]),
                PolystickEdge([self.head, tuple_add(self.head, (1, 0))]),
                PolystickEdge([self.head, tuple_add(self.head, (0, -1))])
            ]
        else:
            return [
                PolystickEdge([self.tail, tuple_add(self.tail, (1, 0))]),
                PolystickEdge([self.tail, tuple_add(self.tail, (-1, 0))]),
                PolystickEdge([self.tail, tuple_add(self.tail, (0, -1))]),
                PolystickEdge([self.head, tuple_add(self.head, (0, 1))]),
                PolystickEdge([self.head, tuple_add(self.head, (1, 0))]),
                PolystickEdge([self.head, tuple_add(self.head, (-1, 0))])
            ]

class Polystick:
    def __init__(self, edges):
        self.edges = edges

    # canonical form: bottom left edge is [(-1,0),(0,0)] or [(0,0),(0,1)]
    def canonical_form(self):
        y0 = min([edge.tail[1] for edge in self.edges])
        bottom_row = [edge for edge in self.edges if edge.tail[1] == y0]
        x0 = min([edge.tail[0] for edge in bottom_row])
        bottom_left_edges = [edge for edge in bottom_row if edge.tail[0] == x0]

        if any([edge.is_vertical() for edge in bottom_left_edges]):
            offset = (-x0, -y0)
        else:
            offset = (-1 - x0, -y0)

        return Polystick(
            [PolystickEdge([tuple_add(edge.tail, offset),
                            tuple_add(edge.head, offset)])
             for edge in self.edges])

    def __eq__(self, other):
        # assuming both are in canonical form
        return set(self.edges) == set(other.edges)

    def __hash__(self):
        return 0

    def rotate(self):
        return Polystick(
            [PolystickEdge([(-edge.tail[1], edge.tail[0]),
                            (-edge.head[1], edge.head[0])])
             for edge in self.edges]).canonical_form()

    def reflect(self):
        return Polystick(
            [PolystickEdge([(edge.tail[0], -edge.tail[1]),
                            (edge.head[0], -edge.head[1])])
             for edge in self.edges]).canonical_form()

    def __repr__(self):
        reprStr = '\n'
        minX = min([edge.tail[0] for edge in self.edges])
        maxX = max([edge.head[0] for edge in self.edges])
        minY = min([edge.tail[1] for edge in self.edges])
        maxY = max([edge.head[1] for edge in self.edges])

        # bitfield
        # N = 0b1000
        # E = 0b0100
        # S = 0b0010
        # W = 0b0001
        for y in range(maxY, minY - 1, -1):
            for x in range(minX, maxX + 1):
                directions = 0
                edges = [edge for edge in self.edges if edge.tail == (x,y)]
                if len(edges) == 2:
                    directions |= 0b1100
                elif len(edges) == 1:
                    if edges[0].is_vertical():
                        directions |= 0b1000
                    else:
                        directions |= 0b0100
                edges = [edge for edge in self.edges if edge.head == (x,y)]
                if len(edges) == 2:
                    directions |= 0b0011
                elif len(edges) == 1:
                    if edges[0].is_vertical():
                        directions |= 0b0010
                    else:
                        directions |= 0b0001
                if directions == 0b0000:
                    reprStr += " "
                elif directions == 0b0001:
                    reprStr += "╴"
                elif directions == 0b0010:
                    reprStr += "╷"
                elif directions == 0b0011:
                    reprStr += "┐"
                elif directions == 0b0100:
                    reprStr += "╶"
                elif directions == 0b0101:
                    reprStr += "─"
                elif directions == 0b0110:
                    reprStr += "┌"
                elif directions == 0b0111:
                    reprStr += "┬"
                elif directions == 0b1000:
                    reprStr += "╵"
                elif directions == 0b1001:
                    reprStr += "┘"
                elif directions == 0b1010:
                    reprStr += "│"
                elif directions == 0b1011:
                    reprStr += "┤"
                elif directions == 0b1100:
                    reprStr += "└"
                elif directions == 0b1101:
                    reprStr += "┴"
                elif directions == 0b1110:
                    reprStr += "├"
                else:
                    reprStr += "┼"
            reprStr += "\n"
        return reprStr


    def __add__(self, other):
        return Polystick(list(set(self.edges + other.edges)))

# redelmeier/malkis algorithm for generating polysticks with up to P edges
def redelmeier(parent, untried, polysticks, P):
    while len(untried) > 0:
        edge = untried.pop()
        child = parent + Polystick([edge])
        polysticks.append(child)
        if len(child.edges) < P:
            new = []
            for neighbor in edge.neighbors():
                if is_new(neighbor, parent):
                    new.append(neighbor)
            polysticks = redelmeier(child, untried + new, polysticks, P)
    return polysticks

def is_new(neighbor, parent):
    #border
    if neighbor.tail[1] < 0:
        return False
    if neighbor.tail[0] < 0 and neighbor.tail[1] == 0:
        return False
    # occupied
    if neighbor in parent.edges:
        return False
    # reachable
    for edge in parent.edges:
        if neighbor in edge.neighbors():
            return False
    # free
    return True

# if a polystick is not the dual graph of a tangle, then return -1
# if it is, then return the number of squares
def is_tangle(polystick):
    G = nx.Graph()

    for edge in polystick.edges:
        G.add_edge(edge.tail, edge.head)

    if nx.is_tree(G):
        return 0

    cycles = nx.cycle_basis(G)
    cycle_lengths = [len(C) for C in cycles]
    squares = sum(1 for m in cycle_lengths if m == 4)

    if squares == len(cycle_lengths):
        return squares
    else:
        return -1

class Tangle:
    def __init__(self, polystick, squares):
        self.edges = polystick.edges
        self.squares = squares
        self.size = len(self.edges)
        self.class_ = self.size - 2 * self.squares + 1
        self.length = 4 * self.class_

def generate_tangles(P):
    fixed_tangles = [[[] for j in range(P + 2)] for i in range(P + 1)]
    onesided_tangles = [[[] for j in range(P + 2)] for i in range(P + 1)]
    free_tangles = [[[] for j in range(P + 2)] for i in range(P + 1)]

    polysticks = redelmeier(Polystick([]),
                            [PolystickEdge([(-1, 0), (0, 0)])], [], P)
    polysticks += redelmeier(Polystick([]),
                             [PolystickEdge([(0, 0), (0, 1)])], [], P)
    for polystick in polysticks:
        squares = is_tangle(polystick)
        if squares > -1:
            m = len(polystick.edges)
            c = m - 2 * squares + 1
            fixed_tangles[m][c].append(polystick)

    # include the circle since it's not found by redelmeier
    fixed_tangles[0][1].append(Polystick([]))
    onesided_tangles[0][1].append(Polystick([]))
    free_tangles[0][1].append(Polystick([]))

    for m in range(1, P + 1):
        for c in range(1, P + 2):
            fixed = fixed_tangles[m][c].copy()
            onesided = []
            free = []
            while len(fixed) > 0:
                tangle = fixed.pop()
                onesided.append(tangle)
                for i in range(4):
                    try:
                        tangle = tangle.rotate()
                        fixed.remove(tangle)
                    except ValueError:
                        pass
            onesided_tangles[m][c] = onesided.copy()
            while len(onesided) > 0:
                tangle = onesided.pop().reflect()
                free.append(tangle)
                for i in range(4):
                    try:
                        tangle = tangle.rotate()
                        onesided.remove(tangle)
                    except ValueError:
                        pass
            free_tangles[m][c] = free
    return (fixed_tangles, onesided_tangles, free_tangles)
