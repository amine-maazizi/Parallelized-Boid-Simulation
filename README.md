# Parallelized Boid Simulation
## Overview
This project implements a simulation of Boids, a flocking behavior model originally developed by Craig Reynolds in 1986. Boids simulate the collective motion of entities (e.g., birds, fish) based on simple rules: separation (avoiding collisions), alignment (matching velocity with neighbors), and cohesion (staying close to the group). This simulation uses Python with Pygame for visualization and is designed to model these emergent behaviors in a 2D space.

The current implementation is single-threaded, with plans to parallelize it using MPI (Message Passing Interface) for improved performance with large numbers of Boids.

## What Are Boids?
Boids are an artificial life program that mimics the flocking behavior of birds or other grouped entities. The model operates on three core principles:

- **Separation**: Steer to avoid crowding nearby Boids.
- **Alignment**: Steer towards the average heading of nearby Boids.
- **Cohesion**: Steer to move toward the average position of nearby Boids.
- Additional rules, like avoiding screen edges or introducing bias (e.g., towards a food source), can enhance the realism of the simulation.

## Code Structure
The project is organized into two main modules:

1. boids.py:
  - Defines the Boid class, which encapsulates the state (position, velocity) and behavior of an individual Boid.
  - Implements the three core rules (separation, alignment, cohesion) plus extras like edge avoidance, speed limits, and group bias.
  - Handles rendering each Boid as a small circle on the screen.
2. engine.py:
  - Defines the Engine class, which manages the simulation loop, initializes Boids, and coordinates their updates and rendering.
  - Uses Pygame to create a window, process events, and draw the simulation.
  - Calculates neighbor interactions within visual and protected ranges for each Boid.

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/amine-maazizi/Parallelized-Boid-Simulation.git
cd Parallelized-Boid-Simulation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulation:
```bash
python main.py
```

## Future Work: Parallelization with MPI
The simulation currently processes all Boids sequentially, which can become slow with large numbers (e.g., thousands). Parallelizing it using MPI will distribute the workload across multiple processes or nodes. Below is a TODO list for this enhancement:

### TODO List
- [ ] **Install MPI**: Set up an MPI implementation (e.g., MPICH or OpenMPI) and the `mpi4py` Python package (`pip install mpi4py`).
- [ ] **Partition Boids**: Divide the Boid population across processes (e.g., split by index or spatial domains).
- [ ] **Synchronize Positions**: Use MPI to broadcast or gather Boid positions/velocities for neighbor calculations.
- [ ] **Optimize Neighbor Search**: Implement a spatial partitioning scheme (e.g., grid-based) to reduce communication overhead, then parallelize across processes.
- [ ] **Handle Ghost Cells**: Add ghost cells (buffer zones) to each process’s spatial domain to share Boid data near boundaries, ensuring accurate interactions between Boids in adjacent MPI processes.
- [ ] **Parallel Process Method**: Update the `Engine.process()` method to compute Boid interactions in parallel, using MPI send/receive for boundary data (including ghost cell updates).
- [ ] **Test Scalability**: Benchmark performance with increasing Boid counts (e.g., 500, 5000, 50000) and processes.
