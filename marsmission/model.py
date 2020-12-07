from __future__ import annotations

from collections import namedtuple
from enum import Enum
from typing import List, Optional

Coordinate = namedtuple('Coordinate', 'x y')


class Direction(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)


class Instruction(Enum):
    L = 'L'
    R = 'R'
    M = 'M'


class Grid:
    def __init__(self, necorner: Coordinate):
        self.xlen = necorner.x + 1
        self.ylen = necorner.y + 1
        self.cells: List[Optional[Rover]] = self.xlen * self.ylen * [None]

    def __contains__(self, point: Coordinate):
        return 0 <= point.x < self.xlen and 0 <= point.y < self.ylen

    def __getitem__(self, point: Coordinate) -> Optional[Rover]:
        return self.cells[point.x + point.y * self.xlen]

    def __setitem__(self, point: Coordinate, rover: Optional[Rover]):
        self.cells[point.x + point.y * self.xlen] = rover


class Rover:
    def __init__(self, grid: Grid, position: Coordinate, heading: Direction):
        if position not in grid:
            raise ValueError("Rover position is outside the grid")
        if grid[position] is not None:
            raise ValueError("The grid position is already occupied")

        grid[position] = self

        self.grid = grid
        self.position = position
        self.heading = heading
        self.instructions = []

    def go(self):
        for instruction in self.instructions:
            if instruction == Instruction.L:
                self.left()
            elif instruction == Instruction.R:
                self.right()
            elif instruction == Instruction.M:
                self.move()

    def _rotate(self, rotation):
        # rotation is a 2-tuple consisting of the nonzero elements of a 2x2 rotation matrix
        self.heading = Direction((rotation[0] * self.heading.value[1], rotation[1] * self.heading.value[0]))

    def left(self):
        self._rotate((-1, 1))

    def right(self):
        self._rotate((1, -1))

    def move(self):
        oldpos = self.position
        newpos = Coordinate(
            x=self.position.x + self.heading.value[0],
            y=self.position.y + self.heading.value[1],
        )
        # ignore invalid move instruction
        if newpos in self.grid and self.grid[newpos] is None:
            self.grid[oldpos] = None
            self.grid[newpos] = self
            self.position = newpos
