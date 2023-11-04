import numpy as np
import math
from pygame import Rect, draw, surface

from utils import check_points

class BasePart:
    def __init__(self, pos : np.ndarray([0,0]), shape : np.ndarray, color : np.ndarray, screen:surface.Surface):
        self.origin = np.array([pos[0],pos[1]])
        self.children = []
        self.display = screen
        self.color = color
        self.state = np.array([[pos[0],pos[1]], [0,0], [0,0]], dtype=float) # [pos, vel, accel]
        self.boundary = list(screen.get_size())
        self.shape = shape
        self.points = shape + self.state[0]
        _, self.state = check_points(self.points, self.state, self.boundary)
        self.points = shape + self.state[0]
        
    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] += x; self.state[0][1] += y

    def draw(self) -> None:
        self.points = self.shape + self.state[0]
        draw.polygon(self.display, self.color, self.points)

class Motor(BasePart):
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface):
        self.radius = 10
        self.shape = np.array([[self.radius, 0], [0, self.radius], [-self.radius, 0], [0, -self.radius]]) # Estimate shape for BasePart
        self.color = np.array([100,100,10,100])
        super().__init__(pos, self.shape, self.color, screen)
    
    def draw(self) -> None:
        draw.circle(self.display, self.color, self.state[0], self.radius)

class Arm(BasePart):
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface):
        self.shape = np.array([[10, 25], [-10, 25], [-10, -25], [10, -25]])
        self.color = np.array([200,100,100,100])
        super().__init__(pos, self.shape, self.color, screen)

class BasePlate(BasePart):
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface):
        self.shape = np.array([[50, 25], [-50, 25], [-25, 0], [25, 0]])
        self.color = np.array([100,100,100,100])
        super().__init__(pos, self.shape, self.color, screen)