# Swarm Simulation

## Problem

This project investigates how a decentralized swarm of autonomous robots can efficiently collect resources in an unknown environment without relying on a central controller. The simulation explores how simple local behaviors produce coordinated group behaviors and examines how environmental uncertainty and root failures affect the swarm's overall performance.

---

## Approach

Each robot operates independently using only local information. Robots begin by exploring the environment through random movement. When a resource enters a robot's sensing radius, the robot moves toward its perceived location, collects the resource, and returns it to a central collection base. During the return trip,  the robot deposits pheromone trails that other robots can detect and follow, improving the swarm's ability to locate additional resources over time.

The simulation was developed incrementally across ten versions (Python Version 3.11.9), beginning with random exploration and gradually introducing resource collection, robot states, pheromone communication, robot failures, sensor noise, and performance metrics.

---

## Decentralization Strategy

The swarm uses a decentralized control strategy inspired by ant colonies. Rather than communicating directly, robots coordinate through digital pheromone trails.

When a robot successfully returns to the base, it leaves pheromones along its path. Nearby robots can detect these trails and preferentially explore those regions, allowing successful paths to emerge naturally without centralized planning. The pheromones gradually evaporate over time, preventing outdated information from persisting indefinitely and enabling the swarm to adapt to changing environments.

---

## Experimental Setup

Four experimental conditions were used to evaluate the robustness of the swarm algorithm:

* **Baseline:** No robot failures and no sensor noise.
* **Failures Only:** Robot failure rates of 0.05%, 0.1&, and 0.2%
* **Noise Only:** Sensor noise levels of 20 px(low), 50 px(medium), and 100 px(high) with no robot failures.
* **Failures + Noise:** Combined robot failures and sensor noise to evaluate swarm performance under multiple simultaneous disturbances.

There were 10 trials conducted for each specific experiment. (100 Trials Total)

All other simulation parameters, including swarm size, sensing radius, pheromone radius, and resource count, were held constant across experiments.

Performance was evaluated using:

* Resources Collected
* Collection rate (resources per simulated second)
* Completion percentage
* Remaining active robots
* Total simulated completion time

Simulation metrics were recorded throughout each run and exported to CSV files for later analysis and visualization.





