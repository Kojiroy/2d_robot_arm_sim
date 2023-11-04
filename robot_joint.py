import numpy as np
import math
from pygame import Rect, draw, surface

from utils import find_nearest, find_lowest, find_highest

class PolyRect:
    # A rectangle made out of polygon lines. Makes it easier to abstract this system to
    # matplotlib.
    def __init__(self, pos : np.ndarray([0,0]), size : np.ndarray([0,0]), rotation: float(0), origin : np.array([0.5,0.5]), color : np.array([10,180,200, 200])):
        self.pos = pos
        self.size = size
        self.rotation = rotation # in radians
        self.color = color
        self.origin = origin # 0 to 1, where 0.5 is the center and 0 is the left or down
        self.points = np.zeros((4,2), dtype=float) # Points are [top_right, bottom_left, top_left, bottom_right] Default settings for polygons, not my choice lol
        self.update_points()

    def rotate(self, val : float = 0.0, degrees : bool = True) -> bool: # TODO: Add rotation relative to specific origin
        # Returns True if rotations 
        self.rotation += math.radians(val) if degrees else val
        self.rotation %= 2 * math.pi

    def move(self, x:float=0, y:float=0) -> None:
        self.pos[0] = x; self.pos[1] = y

    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.pos[0] += x; self.pos[1] += y

    def update_points(self) -> None: #TODO: Need to make rotations relative to origin
        rotation_mat = np.array([[math.cos(self.rotation), -math.sin(self.rotation)], [math.sin(self.rotation), math.cos(self.rotation)]])
        h = np.array([math.hypot(self.size[1] * (1-self.origin[1]),self.size[0] * (1-self.origin[0])),  math.hypot(self.size[1] * (1-self.origin[1]),self.size[0] * self.origin[0]),
                     math.hypot(self.size[1] * self.origin[1],self.size[0] * self.origin[0]), math.hypot(self.size[1] * self.origin[1], self.size[0] * (1-self.origin[0]))])
        feta = np.array([math.atan((self.size[1] * (1-self.origin[1]))/(self.size[0] * (1-self.origin[0]))), math.pi - math.atan((self.size[1] * (1-self.origin[1]))/(self.size[0] * self.origin[0])), 
                       (math.atan((self.size[1] * self.origin[1])/(self.size[0] * self.origin[0])) + math.pi), -math.atan((self.size[1] * self.origin[1])/(self.size[0] * (1-self.origin[0])))], 
                       dtype=float)
        for i in range(4):
            relative_point = np.array([h[i]*math.cos(feta[i]), h[i]*math.sin(feta[i])])
            rotated_point = np.matmul(rotation_mat, relative_point.T)
            self.points[i] = [rotated_point[0] + self.pos[0], rotated_point[1] + self.pos[1]]
            # self.points[i] = [relative_point[0] + self.pos[0], relative_point[1] + self.pos[1]]
            print(f"h: {h}, feta: {feta}, point: {self.points[i]}")
            

    def draw(self, screen:surface.Surface) -> None:
        # print(f"Screen type: {type(screen)}")
        self.update_points()
        draw.polygon(screen, self.color, self.points)
    
    def get_corners(self) -> np.ndarray:
        return self.points
    
    def show_corners(self, screen:surface.Surface) -> None: # I, III, IV, II
        colors = [(255,0,0), (0,255,0), (0,0,255), (0,0,0)]
        origin = [self.pos[0], self.pos[1]]
        for i in range(4):
            draw.line(screen, colors[i], (self.points[i][0], self.points[i][1]), origin)

class RobotJoint: # Has no image
    def __init__(self, name : str = "unamed_joint", pos : np.array = np.array([0,0]), rotation: float = 0, origin : np.array = np.array([0.5,0.5]), size : np.array = np.array([1,1]), color: np.array=([10,180,200, 200]), boundary : np.array=np.array([350,350])) -> None:
        self.name = name
        self.origin = origin # Origin of rotation
        self.boundary = boundary
        self.rect = PolyRect(pos=pos, size=size, rotation=rotation, origin=origin, color=color)
        self.state = np.array([[pos[0],pos[1]], [0,0], [0,0]], dtype=float) # [pos, vel, accel]
        
    def set_vel(self, vel : np.array([0,0])) -> None:
        self.state[1] = vel

    def set_rot(self, degrees: float=0.0) -> None:
        self.rotate(degrees)

    def rotate(self, degrees : float = 0.0) -> None: # TODO: Complete Rotation
        # Rotates an object relative to its current relative position
        self.rect.rotate(degrees)

    def update_state(self, time_step : float = 1) -> None:
        print(f"State prior to update:\n{self.state}")
        self.state[0] += self.state[1] * time_step
        self.move(self.state[1][0], self.state[1][1])
        print(f"State after update:\n{self.state}")
        print(f"Printing origin: {self.origin}")

    def move(self, x : float = 0, y : float = 0) -> bool: # Tested
        # Return false if it hits something, true if movement is safe.
        hit = False
        # calculate the movement
        self.rect.move_ip(x,y)

        # Reset x, y
        x = y = 0
        # Correct Movement
        # Returns True if it moves fine. False otherwise

        # corners = np.asarray([self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])
        corners = self.rect.get_corners()
        # print(corners)
        # print(type(corners))
        lowest_x = find_lowest(corners[:, 0])
        lowest_y = find_lowest(corners[:, 1])
        highest_x = find_highest(corners[:, 0])
        highest_y = find_highest(corners[:, 1])
        # print(f"Printing corners:\n{corners}")
        if lowest_x < 0 :
            x = -lowest_x # Becomes positive
            self.state[1][0] *= -1 if self.state[1][0] < 0 else 1
            hit = True
            # print(f"Hit left side with {lowest_x}")
        elif highest_x > self.boundary[0]:
            x = -highest_x + self.boundary[0] # Becomes negative
            self.state[1][0] *= -1 if self.state[1][0] > 0 else 1
            hit = True
            # print(f"Hit right side with {highest_x}")
        
        if lowest_y < 0:
            y = -lowest_y # becomes positive
            self.state[1][1] *= -1 if self.state[1][1] < 0 else 1
            hit = True
            # print(f"Hit floor with {lowest_y}")
        elif highest_y > self.boundary[1]:
            y = -highest_y + self.boundary[1] # Becomes negative
            self.state[1][1] *= -1 if self.state[1][1] > 0 else 1
            hit = True
            # print(f"Hit ceil with {highest_x}")
        
        self.rect.move_ip(x,y)
        return not hit
    
    def draw(self, screen):
        # draw.line(screen, (0,0,0), self.pos, )
        self.rect.draw(screen)
        self.rect.update_points()
        self.rect.show_corners(screen)