#!/usr/bin/env python

import fileinput

from marsmission.controller import MissionController

if __name__ == '__main__':
    mission_controller = MissionController()
    for line in fileinput.input():
        if (line := line.rstrip()) == ';':
            break
        mission_controller.input(line)
    mission_controller.run()
    for line in mission_controller.output():
        print(line)
