# VERSION 7 - WORKING PHEROMONE TRAILS

import pygame
import random
import math

pygame.init()

# ------------------------
# WINDOW SETTINGS
# ------------------------

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swarm Version 7")

clock = pygame.time.Clock()

# ------------------------
# SWARM SETTINGS
# ------------------------

BASE_X = WIDTH // 2
BASE_Y = HEIGHT // 2

SENSING_RADIUS = 100
COLLECTION_RADIUS = 5
PHEROMONE_RADIUS = 75

resources_collected = 0

# ------------------------
# DATA STRUCTURES
# ------------------------

robots = []
resources = []
pheronomes = []

# ------------------------
# CREATE ROBOTS
# ------------------------

for i in range(20):

    robots.append([

        random.randint(0, WIDTH),   # x

        random.randint(0, HEIGHT),  # y

        False                       # carrying?
    ])

# ------------------------
# CREATE RESOURCES
# ------------------------

for i in range(30):

    resources.append([

        random.randint(0, WIDTH),

        random.randint(0, HEIGHT)

    ])

# ------------------------
# MAIN LOOP
# ------------------------

running = True

while running:

    # ------------------------
    # EVENTS
    # ------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # ------------------------
    # CLEAR SCREEN
    # ------------------------

    screen.fill((0, 0, 0))

    # ------------------------
    # DRAW BASE
    # ------------------------

    pygame.draw.circle(

        screen,

        (0, 0, 255),

        (BASE_X, BASE_Y),

        15

    )

    # ------------------------
    # DRAW RESOURCES
    # ------------------------

    for resource in resources:

        pygame.draw.circle(

            screen,

            (0, 255, 0),

            (resource[0], resource[1]),

            3

        )

    # ------------------------
    # UPDATE ROBOTS
    # ------------------------

    for robot in robots:

        carrying = robot[2]

        # ------------------------
        # SEARCH MODE
        # ------------------------

        if not carrying:
            target_pheromone = None

            target_resource = None

            for pheromone in pheronomes:
                
                distance_to_pheromone = math.sqrt( (robot[0] - pheromone[0])**2 + (robot[1] - pheromone[1])**2)

                if distance_to_pheromone < PHEROMONE_RADIUS:

                    target_pheromone = pheromone
                    break

            for resource in resources:

                distance_to_target = math.sqrt(

                    (robot[0] - resource[0]) ** 2 +

                    (robot[1] - resource[1]) ** 2

                )

                if distance_to_target < SENSING_RADIUS:

                    target_resource = resource

                    break

            if target_resource is not None:

                # Move toward resource

                if target_resource[0] > robot[0]:
                    robot[0] += 2

                elif target_resource[0] < robot[0]:
                    robot[0] -= 2

                if target_resource[1] > robot[1]:
                    robot[1] += 2

                elif target_resource[1] < robot[1]:
                    robot[1] -= 2

                # Recalculate distance after movement

                distance_to_target = math.sqrt(

                    (robot[0] - target_resource[0]) ** 2 +

                    (robot[1] - target_resource[1]) ** 2

                )

                # Collect resource

                if distance_to_target < COLLECTION_RADIUS:

                    if target_resource in resources:

                        resources.remove(target_resource)

                        resources_collected += 1

                        robot[2] = True

            #resrouce speed = 2, pheromone speed = 1 so resources have a stronger attraction
            elif target_pheromone is not None: 
                
                if target_pheromone[0] > robot[0]:
                    robot[0] += 1
                elif target_pheromone[0] < robot[0]:
                    robot[0] -= 1

                if target_pheromone[1] > robot[1]:
                    robot[1] += 1
                elif target_pheromone[1] < robot[1]:
                    robot[1] -= 1
            
            
            else:

                # Random exploration

                robot[0] += random.randint(-2, 2)

                robot[1] += random.randint(-2, 2)

        # ------------------------
        # RETURN MODE
        # ------------------------

        else:

            # Leave pheromone trail

            pheronomes.append([

                robot[0],

                robot[1],

                255

            ])

            # Move toward base

            if BASE_X > robot[0]:
                robot[0] += 2

            elif BASE_X < robot[0]:
                robot[0] -= 2

            if BASE_Y > robot[1]:
                robot[1] += 2

            elif BASE_Y < robot[1]:
                robot[1] -= 2

        # ------------------------
        # DEPOSIT RESOURCE
        # ------------------------

        distance_to_base = math.sqrt(

            (robot[0] - BASE_X) ** 2 +

            (robot[1] - BASE_Y) ** 2

        )

        if robot[2] and distance_to_base < 10:

            robot[2] = False

        # ------------------------
        # KEEP INSIDE WINDOW
        # ------------------------

        robot[0] = max(0, min(WIDTH, robot[0]))

        robot[1] = max(0, min(HEIGHT, robot[1]))

        # ------------------------
        # DRAW ROBOT
        # ------------------------

        pygame.draw.circle(

            screen,

            (255, 255, 0) if robot[2] else (255, 255, 255),

            (int(robot[0]), int(robot[1])),

            5

        )

    # ------------------------
    # DRAW PHEROMONES
    # ------------------------

    for pheromone in pheronomes:

        pygame.draw.circle(

            screen,

            (0, 0, pheromone[2]),

            (int(pheromone[0]), int(pheromone[1])),

            2

        )

    # ------------------------
    # EVAPORATE PHEROMONES
    # ------------------------

    for pheromone in pheronomes:

        pheromone[2] = max(

            0,

            pheromone[2] - 1

        )

    # ------------------------
    # REMOVE DEAD PHEROMONES
    # ------------------------

    new_pheronomes = []

    for p in pheronomes:

        if p[2] > 0:

            new_pheronomes.append(p)

    pheronomes = new_pheronomes

    # ------------------------
    # DISPLAY
    # ------------------------

    pygame.display.flip()

    clock.tick(30)

pygame.quit()

print("Resources Collected:", resources_collected)
