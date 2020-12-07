import re
from enum import Enum

# noinspection PyUnresolvedReferences
from marsmission.model import Grid, Rover, Coordinate, Direction, Instruction

initgrid_re = re.compile(r'^(\d+) (\d+)$')
initrover_re = re.compile(r'^(\d+) (\d+) ([NESW])$')
instructrover_re = re.compile(r'^[LRM]*$')


class InputState(Enum):
    initgrid = 0
    initrover = 1
    instructrover = 2


class MissionController:
    def __init__(self):
        self.inputstate = InputState.initgrid
        self.plateau = None
        self.rovers = []

    def input(self, line: str):
        parse_fn = eval(f'self._parse_{self.inputstate.name}')
        parse_fn(line)

    def run(self):
        for rover in self.rovers:
            rover.go()

    def output(self):
        for rover in self.rovers:
            yield f'{rover.position.x} {rover.position.y} {rover.heading.name}'

    def _parse_initgrid(self, line: str):
        if not (m := initgrid_re.match(line)):
            raise ValueError("Invalid grid initialization line")

        self.plateau = Grid(Coordinate(*map(int, m.groups())))
        self.inputstate = InputState.initrover

    def _parse_initrover(self, line: str):
        if not (m := initrover_re.match(line)):
            raise ValueError("Invalid rover initialization line")

        self.rovers += [Rover(
            grid=self.plateau,
            position=Coordinate(*map(int, m.group(1, 2))),
            heading=eval(f'Direction.{m.group(3)}'),
        )]
        self.inputstate = InputState.instructrover

    def _parse_instructrover(self, line: str):
        if not instructrover_re.match(line):
            raise ValueError("Invalid rover instruction line")

        self.rovers[-1].instructions = list(map(Instruction, tuple(line)))
        self.inputstate = InputState.initrover
