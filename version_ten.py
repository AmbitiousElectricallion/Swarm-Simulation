# VERSION 10 - DATA COLLECTION AND METRICS AND FINISHING TOUCHES

import pygame
import random
import math
import csv
import os

pygame.init()

experiment_number = 1

#--------------
# CREATING METRIC CSV
#--------------

if os.path.isfile("metrics.csv"):

    with open("metrics.csv", "r") as file:

        lines = file.readlines()

        if len(lines) > 1:

            experiment_number = int(lines[-1].split(",")[0]) + 1

# ------------------------
# WINDOW SETTINGS
# ------------------------

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Swarm Version 10")

clock = pygame.time.Clock()
simulation_steps = 0

font = pygame.font.SysFont(None, 30)
start_time = pygame.time.get_ticks()
next_record_time = 1 #Used for getting instantaneous results

# ------------------------
# SWARM SETTINGS
# ------------------------

BASE_X = WIDTH // 2
BASE_Y = HEIGHT // 2

#Metrics to stay constant across all experiments

SENSING_RADIUS = 25
COLLECTION_RADIUS = 5
PHEROMONE_RADIUS = 50
SWARM_SIZE = 50
INITIAL_RESOURCE_COUNT = 100

#Metrics to change for the experimentation

FAILURE_RATE = 0 #manipulated
NOISE_STD = 0 # manipulated



resources_collected = 0

# ------------------------
# DATA
# ------------------------

robots = []
resources = []
pheronomes = []
metrics = []

# ------------------------
# CREATE ROBOTS
# ------------------------

for i in range(SWARM_SIZE):
    robots.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        False,   # carrying
        True     # alive
    ])

# ------------------------
# CREATE RESOURCES
# ------------------------

for i in range(INITIAL_RESOURCE_COUNT):
    resources.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    ])

# ------------------------
# MAIN LOOP
# ------------------------

running = True

while running:

    simulation_steps +=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # base
    pygame.draw.circle(screen, (0, 0, 255), (BASE_X, BASE_Y), 15)

    # resources
    for resource in resources:
        pygame.draw.circle(screen, (0, 255, 0), (resource[0], resource[1]), 3)

    # ------------------------
    # ROBOTS
    # ------------------------

    for robot in robots:

        carrying = robot[2]

        # failure check
        #turns robot off if the condition is met
        if robot[3]:
            if random.random() < FAILURE_RATE:
                robot[3] = False

        # dead robot represented by a red color
        if not robot[3]:
            pygame.draw.circle(screen, (255, 0, 0),
                               (int(robot[0]), int(robot[1])), 5)
            continue

        # ------------------------
        # SEARCH MODE
        # ------------------------

        if not carrying: # Actively Searching

            target_resource = None
            target_pheromone = None

            # pheromone search
            for pheromone in pheronomes:
                # distance between robot and first pheromone trail
                dist = math.sqrt(
                    (robot[0] - pheromone[0]) ** 2 +
                    (robot[1] - pheromone[1]) ** 2
                )
                # Robot catches sight of the trail, locks-in on it.
                if dist < PHEROMONE_RADIUS:
                
                    target_pheromone = pheromone
                    break

            # resource search has the same exact logic relatve to the pheromone search
            for resource in resources:
                dist = math.sqrt(
                    (robot[0] - resource[0]) ** 2 +
                    (robot[1] - resource[1]) ** 2
                )
                if dist < SENSING_RADIUS:
                    target_resource = resource
                    break

            # follow resource (with noise)
            # if a resource is found, robt starts moving towards it, estimatedly 
            if target_resource is not None:

                #introduce some noise to hide the actual location of the reource

                perceived_x = target_resource[0] + random.gauss(0, NOISE_STD)
                perceived_y = target_resource[1] + random.gauss(0, NOISE_STD)

                if perceived_x > robot[0]:
                    robot[0] += 5
                else:
                    robot[0] -= 5

                if perceived_y > robot[1]:
                    robot[1] += 5
                else:
                    robot[1] -= 5

                # Calculate new distance between the robot and resource
                dist_to_target = math.sqrt(
                    (robot[0] - target_resource[0]) ** 2 +
                    (robot[1] - target_resource[1]) ** 2
                )

                if dist_to_target < COLLECTION_RADIUS:
                    if target_resource in resources: #this ensures that if a resrouce is already collected, future robots don't go to it
                        resources.remove(target_resource)
                        resources_collected += 1
                        robot[2] = True

            # follow pheromones if no objects are on target or continue moving randomly
            elif target_pheromone is not None:

                if target_pheromone[0] > robot[0]:
                    robot[0] += 2
                else:
                    robot[0] -= 2

                if target_pheromone[1] > robot[1]:
                    robot[1] += 2
                else:
                    robot[1] -= 2

            else:
                robot[0] += random.randint(-3, 3) # CAN CHANGE THIS METRIC
                robot[1] += random.randint(-3, 3) # CAN CHANGE THIS METRIC

        # ------------------------
        # RETURN MODE
        # ------------------------

        else: #if robot does have an object

            pheronomes.append([robot[0], robot[1], 255]) #this leaves a trail behind
            #robot moves towards the collection base

            if BASE_X > robot[0]:
                robot[0] += 5
            else:
                robot[0] -= 5

            if BASE_Y > robot[1]:
                robot[1] += 5
            else:
                robot[1] -= 5

        # deposit
        dist_base = math.sqrt(
            (robot[0] - BASE_X) ** 2 +
            (robot[1] - BASE_Y) ** 2
        )

        if robot[2] and dist_base < 10: # once it reaches the zone, it is NOT carrying anymore
            robot[2] = False

        # bounds
        robot[0] = max(0, min(WIDTH, robot[0]))
        robot[1] = max(0, min(HEIGHT, robot[1]))

        # draw robot
        pygame.draw.circle(
            screen,
            (255, 255, 0) if robot[2] else (255, 255, 255), #yellow if carryying or just white
            (int(robot[0]), int(robot[1])),
            5
        )

    # ------------------------
    # PHEROMONES
    # ------------------------

    for pheromone in pheronomes:

        pygame.draw.circle(
            screen,
            (0, 0, pheromone[2]),
            (int(pheromone[0]), int(pheromone[1])), # draw trail circle at robot's current position
            2
        )
        # CAN CHANGE THIS METRIC
        pheromone[2] = max(0, pheromone[2] - 2) # evaporating as color value is decreasing

    pheronomes = [p for p in pheronomes if p[2] > 0] # remove dead pheromones

    # ------------------------
    # STATS (LIVE)
    # ------------------------

    alive_robots = sum(1 for r in robots if r[3])

    simulation_time = simulation_steps/30

    collection_rate = (
        resources_collected / simulation_time
        if simulation_time > 0 else 0
    )

    completion_percentage = (
        resources_collected / INITIAL_RESOURCE_COUNT
    ) * 100

    # records the instantaneous time
    if simulation_time >= next_record_time:
        metrics.append([
            experiment_number,
            simulation_time,
            resources_collected,
            alive_robots,
            collection_rate,
            completion_percentage
        ])
        next_record_time += 1

    # draw stats
    screen.blit(font.render(f"Collected: {resources_collected}", True, (255,255,255)), (10,10))
    screen.blit(font.render(f"Alive: {alive_robots}", True, (255,255,255)), (10,40))
    screen.blit(font.render(f"Rate: {collection_rate:.2f}/s", True, (255,255,255)), (10,70))
    screen.blit(font.render(f"Completion: {completion_percentage:.1f}%", True, (255,255,255)), (10,100))

    # program stops once all resources are collected, or once all robots are dead
    if len(resources) == 0 or all(not r[3] for r in robots):
        running = False

    pygame.display.flip()
    clock.tick(10000)

# ------------------------
# FINAL OUTPUT
# ------------------------

pygame.quit()

# create file format for metrics at specifics moments in simulated time

file_exists = os.path.isfile("metrics.csv")

with open("metrics.csv", "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:

        writer.writerow([

            "Experiment",

            "Simulated Time",

            "ResourcesCollected",

            "AliveRobots",

            "CollectionRate",

            "CompletionPercentage"

        ])

    writer.writerows(metrics)

# DISPLAYING END RESULTS

print("Simulation ended: all resources collected or swarm collapsed")

print("Completion Percentage:", completion_percentage)
print("Collection Rate:", collection_rate)
print("Simulated Time:", simulation_time)
print("Resources Collected:", resources_collected)
print("Remaining Robots:", alive_robots)

#------------
# LOADING DATA INTO CSV FILES
#------------


# experiment_summary.csv stores the END results of each experiment
file_exists = os.path.isfile("experiment_summary.csv")

with open("experiment_summary.csv", "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "FailureRate",
            "NoiseStd",
            "SwarmSize",
            "ResourcesCollected",
            "AliveRobots",
            "SimulationTime",
            "CollectionRate",
            "CompletionPercentage"
        ])

    writer.writerow([
        FAILURE_RATE,
        NOISE_STD,
        SWARM_SIZE,
        resources_collected,
        alive_robots,
        simulation_time,
        collection_rate,
        completion_percentage
    ])

    