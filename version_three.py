#VERSION THREE - DETECTING RESOURCES

# Import the pygame library so we can create a window and draw things
import pygame

# Import the random library so robots can move randomly
import random

import math # Used to Calculate Distance Later Between Robot and Resource

# Start all pygame systems
pygame.init()

# Width of the simulation window in pixels
WIDTH = 1000

# Height of the simulation window in pixels
HEIGHT = 800

#How far a robot can "see"

SENSING_RADIUS = 100

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Swarm Version 3")

# Creates a clock object that helps control FPS
clock = pygame.time.Clock()

# Empty list that will store robot positions
robots = []

#Empy list that will store the position of the objects
resources = []


# Create 20 robots
for i in range(20):

    # Add a robot at a random x,y position
    robots.append([

        # Random x coordinate
        random.randint(0, WIDTH),

        # Random y coordinate
        random.randint(0, HEIGHT)

    ])

# Create 30 Resources
for i in range(30):
    resources.append([
        random.randint(0,WIDTH),
        random.randint(0,HEIGHT)
    ])

# Variable that controls whether the simulation keeps running
running = True

# Main game loop
# This loop runs over and over until the user closes the window
while running:

    # Check for user events
    for event in pygame.event.get():

        # If the user clicks the X button
        if event.type == pygame.QUIT:

            # Stop the simulation
            running = False

    # Fill the screen with black
    # This erases everything from the previous frame
    screen.fill((0, 0, 0))

    # Resources are made before the robbots so that if a robot stands directly on a resrouce, you can still see the robot.
    for resource in resources:

        pygame.draw.circle (

            screen,

            (0,255,0),

            (resource[0], resource[1]),

            3
        )

    # Go through every robot
    for robot in robots:

        #Assuming each robot initially sees nothing
        target_resource = None

        #Check every resource

        for resource in resources:

            distance = math.sqrt( (robot[0] - resource[0])**2 + (robot[1] - resource[1])**2 )

            #If the resource is within robot's visual field

            if distance < SENSING_RADIUS:
                target_resource = resource
                break


        if target_resource is not None:
            # Move toward resrouce
            if target_resource[0] > robot[0]:
                robot[0] += 2
            elif target_resource[0] < robot[0]:
                robot[0] -= 2
            if target_resource[1] > robot[1]:
                robot[1] += 2
            elif target_resource[1] < robot[1]:
                robot[1] -= 2 
        else: 
            # Move robot left/right randomly as no resource seen
            robot[0] += random.randint(-2, 2)

            # Move robot up/down randomly
            robot[1] += random.randint(-2, 2)

        # Keep robot inside the window horizontally
        robot[0] = max(0, min(WIDTH, robot[0]))

        # Keep robot inside the window vertically
        robot[1] = max(0, min(HEIGHT, robot[1]))

        # Draw the robot as a white circle
        pygame.draw.circle(

            # Draw on this window
            screen,

            # White color (R,G,B)
            (255, 255, 255),

            # Robot position
            (int(robot[0]), int(robot[1])),

            # Radius of circle
            5

        )

    # Show everything drawn this frame
    pygame.display.flip()

    # Limit simulation speed to 60 FPS
    clock.tick(30)

# Shut down pygame when the program ends
pygame.quit()