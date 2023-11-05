import numpy as np
import math
from pygame import draw, surface

from utils import check_points, find_highest, find_lowest

class BasePart:
    '''
    Everything is Relative
    '''
    def __init__(self, shape : np.ndarray, color : np.ndarray, screen:surface.Surface, pos : np.array = np.array([0,0]), origin : np.array=np.array([0, 0]), rotation: float=0, parent=None):
        self.display = screen
        self.color = color
        self.state = np.array([[pos[0],pos[1]], [0,0], [0,0]], dtype=float) # [pos, vel, accel]
        self.boundary = list(screen.get_size())
        self.shape = shape
        self.rotation = rotation
        self.origin = origin
        self.abs_origin : np.ndarray
        self.parent = parent

        self.num_points = self.shape.shape[0]
        self.points = np.ndarray(shape=(self.num_points,2 ),dtype=float)
        self.update_points()
        check_points(self.points, self.state, self.boundary)
    
    def rotate_ip(self, val : float = 0.0, degrees : bool = True) -> bool: # TODO: Add rotation relative to specific origin
        # Returns True if rotations 
        self.rotation += math.radians(val) if degrees else val
        self.rotation %= 2 * math.pi

    def rotate(self, val : float = 0.0, degrees : bool = True) -> bool: # TODO: Add rotation relative to specific origin
        # Returns True if rotations 
        self.rotation = math.radians(val) if degrees else val
        self.rotation %= 2 * math.pi

    def move_ip(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] += x; self.state[0][1] += y

    def move(self, x: float = 0, y: float = 0) -> None:
        self.state[0][0] = x; self.state[0][1] = y

    def update_points(self) -> None:
        shape = np.array([[point[0], point[1], 1] for point in self.shape])
        origin = np.hstack((self.origin, 1))
        transf_mat = self.get_transf_mat()
        for i in range(self.num_points):
            self.points[i] = np.matmul(shape[i], transf_mat)[0:2]
        self.abs_origin = np.matmul(origin, transf_mat)[0:2]
        # check_points(self.points, self.state, self.boundary)

    def draw(self) -> None:
        self.update_points()
        draw.polygon(self.display, self.color, self.points)
        self.show_corners()
    
    def get_corners(self) -> np.array:
        return self.points
    
    def show_corners(self) -> None: # I, III, IV, II
        colors = [(255,0,0), (0,255,0), (0,0,255), (0,0,0), (100,0,0), (0,100,0), (0,0,100), (255,255,255),
                  (255,255,10), (255,0,255), (0,255,255), (100,255,0), (100,0,255), (255,100,0), (0,100,255), (255,255,100)]
        # origin = [self.state[0][0], self.state[0][1]]
        # print(f"self.points: {self.points}\norigin:{origin}")
        for i in range(self.num_points):
            draw.line(self.display, colors[i], (self.points[i][0], self.points[i][1]), self.abs_origin)

    def add_child(self, part, origin):
        self.children.append([part, origin])
        part.parent(self)
    
    def get_transf_mat(self)->np.ndarray:
        parent_transf_mat = np.eye(3) if self.parent == None else self.parent.get_transf_mat()
        trans_transf_mat = np.array([[1, 0, 0], [0,1,0], [self.state[0][0], self.state[0][1], 1]])
        parent_transf_mat = np.matmul(trans_transf_mat, parent_transf_mat)
        cur_transf_mat = np.array([[math.cos(self.rotation), -math.sin(self.rotation), 0],
                         [math.sin(self.rotation), math.cos(self.rotation), 0,],
                         [self.origin[0] * math.cos(self.rotation) + self.origin[1] * math.sin(self.rotation),
                          -self.origin[0] * math.sin(self.rotation) + self.origin[1] * math.cos(self.rotation), 1
                          ]])
        # self.abs_origin = np.matmul()
        # print(f"Parent:\n{parent_transf_mat}\nCur_trans:\n{cur_transf_mat}\nrotation:{self.rotation}")
        return np.matmul(cur_transf_mat, parent_transf_mat)

class Motor(BasePart):
    def __init__(self, screen:surface.Surface, pos : np.ndarray = np.array([0,0]), parent=None):
        self.radius = 10
        self.center = None # Abs center point
        self.shape = np.array([[self.radius, 0], [0, self.radius], [-self.radius, 0], [0, -self.radius]]) # Estimate shape for BasePart
        self.color = np.array([100,100,10,100])
        super().__init__(pos=pos, shape=self.shape, color=self.color, screen=screen, parent=parent)

    def update_points(self) -> None:
        center = np.hstack((self.origin, 1))
        transf_mat = self.get_transf_mat()
        self.center = np.matmul(center, transf_mat)[0:2]
        # print(f"center: {self.center}\npos: {self.state[0]}")
        
    def draw(self) -> None:
        self.update_points()
        draw.circle(self.display, self.color, self.center, self.radius)

class Arm(BasePart):
    def __init__(self, screen:surface.Surface, parent=None):
        self.shape = np.array([[10, 25], [-10, 25], [-10, -25], [10, -25]])
        self.color = np.array([200,100,100,100])
        pos = [0, -25]
        origin = [0, 0]
        
        super().__init__(pos=pos, shape=self.shape, color=self.color, screen=screen, parent=parent, origin=origin)
    
    def get_endpoint(self) -> np.ndarray:
        return (self.shape[3] + self.shape[2])/2

class BasePlate(BasePart):
    def __init__(self, pos : np.ndarray([0,0]), screen:surface.Surface):
        self.shape = np.array([[50, 25], [-50, 25], [-25, 0], [25, 0]])
        origin = np.array([0,0])
        # self.connector = 
        self.color = np.array([100,100,100,100])
        super().__init__(origin=origin, pos=pos, shape=self.shape, color=self.color, screen=screen)

class Claw(BasePart):
    def __init__(self, pos: np.ndarray([0,0]), screen:surface.Surface, name="", parent=None):
        self.name = name
        self.shape = np.array([[15, 25], [-15, 25], [-25, -10], [-7, -25], [-15, -7],
                              [0, 15], [15, -7], [7, -25], [25, -10]]) # Max Size is 50,50
        self.color = np.array([200,0,0, 100])
        origin = np.array([0,-25])
        super().__init__(origin=pos, pos=origin, shape=self.shape, color=self.color,screen=screen, parent=parent)