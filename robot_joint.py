import numpy as np
import math
from pygame import Rect, draw

from utils import find_nearest, find_lowest, find_highest

class PolyRect:
    # A rectangle made out of polygon lines. Makes it easier to abstract this system to
    # matplotlib.
    def __init__(self, pos : np.ndarray([0,0]), size : np.ndarray([0,0]), rotation: np.ndarray([0,0]), color : np.array([10,180,200, 200])):
        self.pos = pos
        self.size = size
        self.rotation = rotation # in radians
        self.color = color
        self.points = np.zeros((4,2), dtype=float)
        self.update_points()

    def rotate(self, val : float = 0.0, degrees : bool = True) -> bool:
        # Returns True if rotations 
        self.rotation = math.radians(val) if degrees else val

    def move_ip(self, x: float = 0, y: float = 0):
        self.pos[0] = x; self.pos[1] = y

    def update_points(self):
        x:float = self.pos[0] + self.size[0]
        y:float = self.pos[1] + self.size[1]
        h:float = 0
        feta:float = 0.0
        for i in range(4):
            x *= -1 if i%2 else 1
            y *= -1 if i/2 else 1
            h = math.hypot(x,y)
            feta = math.atan(y/x) + self.rotation
            self.points[i] = [h*math.cos(feta), h*math.cos(feta)]

    def draw(self, screen):
        print(f"Screen type: {type(screen)}")
        self.update_points()
        draw.polygon(screen, self.color, self.points)

class RobotJoint: # Has no image
    def __init__(self, name : str = "unamed_joint", pos : np.array = np.array([0,0]), origin : np.array = np.array([0,0]), size : np.array = np.array([1,1]), boundary : np.array=np.array([350,350])) -> None:
        self.name = name
        self.origin = origin
        self.boundary = boundary
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
    
    def rotate(self, degrees : float = 0.0) -> None: # TODO: Complete Rotation
        # Rotates an object relative to its current relative position
        pass

    def move(self, x : float = 0, y : float = 0) -> bool: # Tested
        # Return false if it hits something, true if movement is safe.
        hit = False
        # calculate the movement
        self.rect.move_ip(x,y)

        # Reset x, y
        x = y = 0
        # Correct Movement
        # Returns True if it moves fine. False otherwise

        corners = np.asarray([self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])
        print(corners)
        print(type(corners))
        lowest_x = find_lowest(corners[:, 0])
        lowest_y = find_lowest(corners[:, 1])
        highest_x = find_highest(corners[:, 0])
        highest_y = find_highest(corners[:, 1])
        if lowest_x < 0 :
            x = -lowest_x # Becomes positive
            hit = True
        elif highest_x > self.boundary[0]:
            x = -highest_x + self.boundary[0] # Becomes negative
            hit = True
        
        if lowest_y < 0:
            y = -lowest_y # becomes positive
            hit = True
        elif highest_y > self.boundary[1]:
            y = -highest_y + self.boundary[1] # Becomes negative
            hit = True
        
        self.rect.move_ip(x,y)
        return not hit
