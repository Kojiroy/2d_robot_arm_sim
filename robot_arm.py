import numpy as np
import math
from pygame import Rect, draw, surface

from utils import check_points
from robot_parts import BasePlate, Claw, Motor
from robot_joint import RobotJoint

class RobotArm:
    # A rectangle made out of polygon lines. Makes it easier to abstract this system to
    # matplotlib.
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface): # Sets the position of the base of the robot
        self.base = BasePlate(pos, screen)
        self.first_joint = RobotJoint(screen=screen, parent=self.base, name="First Joint")
        self.second_joint = RobotJoint(screen=screen, parent=self.first_joint.children[-1], name="Second Joint", pos=self.first_joint.edge)
        self.claw = Claw(screen=screen, parent=self.second_joint.children[-1], name="Claw", pos=self.second_joint.edge)
        self.motor = Motor(screen=screen, parent=self.claw)
    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] += x; self.state[0][1] += y
    
    def rotate(self, rotation : float):
        # pass
        self.first_joint.rotate(rotation)
        self.second_joint.rotate(rotation)
        # self.claw.rotate(-rotation)
        # self.base.rotate(rotation)

    def draw(self) -> None:
        # print("drawing base")
        self.base.draw()
        # print("drawing first_joint")
        self.first_joint.draw()
        # print("Drawing second joint")
        self.second_joint.draw()
        # # print("Drawing claw")
        self.claw.draw()
        self.motor.draw()