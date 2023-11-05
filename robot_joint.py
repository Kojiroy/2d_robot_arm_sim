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
        self.state = np.array([[pos[0],pos[1]], [0,0], [0,0]], dtype=float) # [pos, vel, accel]
        self.motor = Motor(pos, screen, parent=parent)
        self.arm = Arm(screen, parent=self.motor)
        self.children = [self.motor, self.arm] # The last index is the edge
        self.edge = self.arm.get_endpoint()
        
    def set_vel(self, vel : np.array([0,0])) -> None:
        self.state[1] = vel

    def rotate(self, degrees : float = 0.0) -> None: # TODO: Complete Rotation
        # Rotates an object relative to its current relative position
        self.motor.rotate(degrees)
        # pass

    def draw(self):
        # draw.line(screen, (0,0,0), self.pos, )
        self.arm.draw()
        self.motor.draw()