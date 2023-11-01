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

test_limb = RobotJoint(name="test", pos=np.array([150,150]), origin=np.array([0,0]), size=np.array([10,30]), boundary=np.array([DISPLAY_WIDTH,DISPLAY_HEIGHT]))

test_limb.set_vel(np.array([1,2]))

robot_limbs = [test_limb]

while running:
    # Update limb states
    fpsClock.tick(60)
    for limb in robot_limbs:
        limb.update_state(1)
        limb.rotate(1)

    display.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # pygame.draw.rect(display, ARM_COLOR, pygame.Rect(50, 30, 20, 60), 5)

    for limb in robot_limbs:
        limb.draw(display)
        # pygame.draw.rect(display, ARM_COLOR, limb.rect)
    pygame.display.update()
    display.fill(BG)
pygame.quit()