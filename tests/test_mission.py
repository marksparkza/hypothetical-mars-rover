import pytest
from hypothesis import given, assume, strategies as hs

from marsmission.controller import MissionController

example_input_1 = \
'''5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM'''

expected_output_1 = \
'''1 3 N
5 1 E'''

example_input_2 = \
'''7 4
2 2 S
MMMRMMMRMLM
1 2 E
MMMMLMMMRMR
5 2 S
LMLMMLMRM'''

expected_output_2 = \
'''0 1 W
5 4 S
6 4 N'''


@pytest.mark.parametrize('example_input, expected_output', [
    (example_input_1, expected_output_1),
    (example_input_2, expected_output_2),
])
def test_mission_example(example_input, expected_output):
    mission_controller = MissionController()
    for line in example_input.split('\n'):
        mission_controller.input(line)
    mission_controller.run()
    actual_output = '\n'.join(list(mission_controller.output()))
    assert actual_output == expected_output


@hs.composite
def mission_scenario(
        draw,
        plateau_xlen=hs.integers(min_value=1, max_value=50),
        plateau_ylen=hs.integers(min_value=1, max_value=50),
):
    grid_xlen = draw(plateau_xlen)
    grid_ylen = draw(plateau_ylen)
    grid_cells = grid_xlen * grid_ylen * [False]
    num_rovers = draw(hs.integers(min_value=0, max_value=len(grid_cells) // 2 + 1))
    rovers = []
    while len(rovers) < num_rovers:
        rover_x = draw(hs.integers(min_value=0, max_value=grid_xlen - 1))
        rover_y = draw(hs.integers(min_value=0, max_value=grid_ylen - 1))
        assume(grid_cells[rover_x + rover_y * grid_xlen] is False)
        grid_cells[rover_x + rover_y * grid_xlen] = True
        rover_head = draw(hs.sampled_from(('N', 'E', 'S', 'W')))
        rover_cmds = draw(hs.text(alphabet=('L', 'R', 'M')))
        rovers += [(rover_x, rover_y, rover_head, rover_cmds)]

    mission_input = f'{grid_xlen} {grid_ylen}'
    for rover in rovers:
        mission_input += f'\n{rover[0]} {rover[1]} {rover[2]}\n{rover[3]}'

    return mission_input


@given(mission_scenario())
def test_mission_scenario(randomized_input):
    print("\n-----INPUT------")
    print(randomized_input)

    mission_controller = MissionController()
    for line in randomized_input.split('\n'):
        mission_controller.input(line)
    mission_controller.run()

    print("-----OUTPUT-----")
    for line in mission_controller.output():
        print(line)
    print("----------------")

    gridded_rovers = [rover for rover in mission_controller.plateau.cells if rover is not None]
    assert len(gridded_rovers) == len(mission_controller.rovers)
    assert set(gridded_rovers) == set(mission_controller.rovers)
    assert all(mission_controller.plateau[rover.position] == rover for rover in mission_controller.rovers)
