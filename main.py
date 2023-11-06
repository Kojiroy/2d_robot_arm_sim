import pygame
import numpy as np
from pygame.locals import *
from robot_arm import RobotArm

running = True
BG = (200,200,200)
ARM_COLOR = (10,180,200, 200)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300

pygame.init()

display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
fpsClock = pygame.time.Clock()

pygame.display.set_caption("Robot Arm")

# robot = RobotArm(np.array([0,0]), display)

# test_limb = RobotJoint(parent=robot, name="test", pos=np.array([150,150]), origin=np.array([0.1,0.1]), size=np.array([10,100]), boundary=np.array([DISPLAY_WIDTH,DISPLAY_HEIGHT]), color=[10,180,200, 20])
# test_limb2 = RobotJoint(parent=robot, name="test", pos=np.array([150,150]), origin=np.array([0.5,0.5]), size=np.array([100,100]), boundary=np.array([DISPLAY_WIDTH,DISPLAY_HEIGHT]), color=(100,100,100,10))

# test_limb.set_vel(np.array([-1,-2]))
# test_limb2.set_vel(np.array([-1,-2]))

robot_arm = RobotArm(np.array([DISPLAY_WIDTH/2,DISPLAY_HEIGHT]), display)
# robot_motor = Motor(np.array([0,0]), display)
# robot_arm = Arm(np.array([DISPLAY_WIDTH,0]), display)
# robot_base = BasePlate(np.array([DISPLAY_WIDTH,DISPLAY_HEIGHT]), display)


# robot_limbs = [test_limb2, test_limb]

while running:
    # Update limb states
    fpsClock.tick(60)
    # for limb in robot_limbs:
    #     limb.update_state(1)
    #     limb.rotate(1)
    # robot_arm.rotate(1)
    display.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                robot_arm.set_angular_velocity(2, 1)
            elif event.key == pygame.K_DOWN:
                robot_arm.set_angular_velocity(-2, 1)
            if event.key == pygame.K_RIGHT:
                robot_arm.set_angular_velocity(2, 0)
            elif event.key == pygame.K_LEFT:
                robot_arm.set_angular_velocity(-2, 0)
                print("Key Pressed")

        if robot_arm.rotating[1]:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    robot_arm.set_angular_velocity(0, 1)
                elif event.key == pygame.K_DOWN:
                    robot_arm.set_angular_velocity(0, 1)
        if robot_arm.rotating[0]:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    robot_arm.set_angular_velocity(0, 0)
                elif event.key == pygame.K_LEFT:
                    print("Key Unpressed")
                    robot_arm.set_angular_velocity(0, 0)

        
    # pygame.draw.rect(display, ARM_COLOR, pygame.Rect(50, 30, 20, 60), 5)

    # for limb in robot_limbs:
    #     limb.draw(display)
        # pygame.draw.rect(display, ARM_COLOR, limb.rect)
    
    # robot_motor.draw()
    robot_arm.update(1)
    robot_arm.draw()
    # robot_base.draw()


    pygame.display.update()
    display.fill(BG)
pygame.quit()