import numpy as np
import math
from pygame import Rect, draw, surface
from robot_parts import BasePlate, BasePart, Arm, Motor

from utils import find_nearest, find_lowest, find_highest, check_points

class RobotJoint:
    '''
    Consists of a motor and arm. The origin of rotation is around the center of the motor.
    pos : the position of the center of the motor
    parent : A BasePart that this joint is connected to this object's motor. Is connected to the edge of the arm
    '''
    def __init__(self, screen:surface.Surface, parent, name : str = "unamed_joint", pos : np.array = np.array([0,0])) -> None:
        self.name = name
        self.screen = screen
        self.parent = parent
        self.state = np.array([0,0,0], dtype=float) # [pos, vel, accel, [rotation, angular rotation, angular acceleration]]
        self.motor = Motor(pos=pos, screen=screen, parent=parent)
        self.arm = Arm(screen, parent=self.motor)
        self.children = [self.motor, self.arm] # The last index is the edge
        self.edge = self.arm.get_endpoint()
        
    def set_angular_vel(self, ang_vel : float = 0) -> None:
        self.state[1] = ang_vel

    def rotate(self, degrees : float = 0.0) -> None: # TODO: Complete Rotation
        # Rotates an object relative to its current relative position
        self.state[0] = degrees

    def update(self, delta_t : float):
        self.state[1] += delta_t * self.state[2]
        self.state[0] += delta_t * self.state[1]
        self.motor.rotate(self.state[0])
        # pass

    def draw(self):
        # draw.line(screen, (0,0,0), self.pos, )
        self.arm.draw()
        self.motor.draw()