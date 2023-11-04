import numpy as np
import math
from pygame import Rect, draw, surface

from utils import check_points

class RobotArm:
    # A rectangle made out of polygon lines. Makes it easier to abstract this system to
    # matplotlib.
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface): # Sets the position of the base of the robot
        pass

    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] += x; self.state[0][1] += y

    def draw(self) -> None:
        draw.polygon(self.display, self.color, self.points)