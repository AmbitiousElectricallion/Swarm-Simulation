#VERSION FIVE - RETURNING RESOURCE TO COLLECTION ZONE

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

BASE_X = WIDTH // 2
BASE_Y = HEIGHT // 2

#How far a robot can "see"
SENSING_RADIUS = 100

#How far a robot can still collect a resource
COLLECTION_RADIUS = 5

#number of objects collected

resources_collected =0


# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Swarm Version 5")

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
        random.randint(0, HEIGHT), 

        False

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

    # blue circle represents collection base
    pygame.draw.circle(
        screen, 
        (0,0,255),
        (BASE_X, BASE_Y),
        15
    )

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
        carrying = robot[2]
        #once robot carries an object, it moves straight to the collection zone
        if not carrying:

            #Assuming each robot initially sees nothing
            target_resource = None

            #Check every resource

            for resource in resources:

                distance_to_target = math.sqrt( (robot[0] - resource[0])**2 + (robot[1] - resource[1])**2 )

                #If the resource is within robot's visual field

                if distance_to_target < SENSING_RADIUS:
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

                #recalculated here so that collection is based on the robot's current position, not its position from an earlier frame

                distance_to_target = math.sqrt((robot[0] - target_resource[0])**2 + (robot[1] - target_resource[1])**2)

                # once robot comes close, it collects object
                #if multiple robots try to collect the same resource during the same frame, it can cause errors.
                #So, adding the nested if statement acts as a safety check

                if distance_to_target < COLLECTION_RADIUS:
                    if target_resource in resources:
                        resources.remove(target_resource)
                        #object counter
                        resources_collected += 1;
                        #change robot state to carrying
                        robot[2] = True
                        
            else: 
                # Move robot left/right randomly as no resource seen
                robot[0] += random.randint(-2,2)

                # Move robot up/down randomly
                robot[1] += random.randint(-2,2)
        else:

            if BASE_X > robot[0]:
                robot[0] += 2
            elif BASE_X < robot[0]:
                robot[0] -= 2
            
            if BASE_Y > robot[1]:
                robot[1] += 2
            elif BASE_Y < robot[1]:
                robot[1] -= 2
        
        distance_to_base = math.sqrt((robot[0] - BASE_X)**2 + (robot[1] - BASE_Y)**2)

        # Once robot reaches the base, it "deposits" object
        
        if robot[2] and distance_to_base < 10:
            robot[2] = False

        # Keep robot inside the window horizontally
        robot[0] = max(0, min(WIDTH, robot[0]))

        # Keep robot inside the window vertically
        robot[1] = max(0, min(HEIGHT, robot[1]))

        # Draw the robot as a white circle
        pygame.draw.circle(

            # Draw on this window
            screen,

            # White color (R,G,B)
            #turns yellow once robot picks up an object
            (255, 255, 0) if robot[2] else (255,255,255),
            
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

print(resources_collected)

