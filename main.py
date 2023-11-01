import pygame
import numpy as np
from pygame.locals import *
from robot_joint import RobotJoint

running = True
BG = (200,200,200)
ARM_COLOR = (10,180,200, 200)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300

pygame.init()

display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Robot Arm")

test_limb = RobotJoint("test", np.array([150,150]), np.array([0,0]), np.array([10,30]), np.array([DISPLAY_WIDTH,DISPLAY_HEIGHT]))
robot_limbs = [test_limb]

x_vel = 1
y_vel = 2

while running:
    # Update limb states
    fpsClock.tick(60)
    for limb in robot_limbs:
        x_vel *= 1 if limb.move(x_vel, 0) else -1
        y_vel *= 1 if limb.move(0, y_vel) else -1

    display.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # pygame.draw.rect(display, ARM_COLOR, pygame.Rect(50, 30, 20, 60), 5)

    for limb in robot_limbs:
        pygame.draw.rect(display, ARM_COLOR, limb.rect)
    pygame.display.update()
    display.fill(BG)
pygame.quit()