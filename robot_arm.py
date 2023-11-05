import numpy as np
import math
from pygame import Rect, draw, surface

from utils import check_points
from robot_parts import BasePlate, Claw, Motor
from robot_joint import RobotJoint

START_ROTATIONS = [-30,-60]
class RobotArm:
    # A rectangle made out of polygon lines. Makes it easier to abstract this system to
    # matplotlib.
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface): # Sets the position of the base of the robot
        self.base = BasePlate(pos, screen)
        self.joints = []
        self.joints.append(RobotJoint(screen=screen, parent=self.base, name="First Joint"))
        self.joints.append(RobotJoint(screen=screen, parent=self.joints[0].children[-1], name="Second Joint", pos=self.joints[0].edge))
        self.claw = Claw(screen=screen, parent=self.joints[1].children[-1], name="Claw", pos=self.joints[1].edge)
        self.num_joints = len(self.joints)
        self.rotating = [False] * self.num_joints
        for i in range(self.num_joints):
            self.joints[i].rotate(START_ROTATIONS[i])

    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] += x; self.state[0][1] += y
    
    def set_angular_rotation(self, angular_vel:float, joint:int=0):
        if angular_vel:
            self.rotating[joint] = True
        self.joints[joint].set_angular_vel(angular_vel)
        # pass

    def rotate(self, rotation : float, joint : int = 0):
        # pass
        self.joints[joint].rotate(rotation)
        # self.claw.rotate(-rotation)
        # self.base.rotate(rotation)
    
    def update(self, delta_t : float) -> None:
        for i in range(self.num_joints):
            self.joints[i].update(delta_t)
            print(f"joint[{i}]:\n{self.joints[i].state}")

    def draw(self) -> None:
        # print("drawing base")
        self.base.draw()
        # print("drawing first_joint")
        self.joints[0].draw()
        # print("Drawing second joint")
        self.joints[1].draw()
        # # print("Drawing claw")
        self.claw.draw()