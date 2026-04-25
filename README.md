# Traffic Network Simulator
**Course:** EE5150 Communication Networks  
**Assignment:** Assignment 6  
**Authors:** 
* J Dattatreya Sastry (EE22B175)  
* K Jaideep Reddy (EE22B013)

---

## Overview
This project is a modular, discrete-time traffic simulator developed to model directional traffic flow within a planar network. The simulator provides a framework to define network topologies, simulate vehicle movement with queuing and scheduling, and visualize results through dynamic animations.

## Core Features
* **Modular Library Architecture:** The simulation logic is encapsulated within the `traffic_sim/` package, ensuring separation of concerns between network components, the simulation engine, and visualization tools.
* **Graph-Based Routing:** Utilizes Dijkstra’s algorithm to calculate the shortest path from a source to a destination node upon vehicle generation.
* **Queuing and Physical Modeling:** Incorporates road capacity limits, physical road lengths, and individual vehicle speeds. Queuing occurs at the end of a road segment when a junction or destination road is occupied.
* **Junction Scheduling:** Implements a Round-Robin scheduling algorithm at junctions to ensure fairness and prevent starvation of incoming road segments.
* **Stochastic Arrival Models:** Supports both a standard Bernoulli process and a Poisson process for vehicle generation. The Poisson model effectively simulates "bursty" traffic arrivals.
* **Visual Representation:** Produces high-fidelity .gif animations. Vehicles are color-coded based on status: Lime circles represent vehicles in transit, while Red squares represent vehicles waiting in a queue.

## Project Structure
```text
A6 - Traffic Network Simulator/
├── traffic_sim/            # Core library module
│   ├── engine.py           # Standard (Bernoulli) simulation engine
│   ├── engine_poisson.py   # Advanced (Poisson) simulation engine
│   ├── network.py          # Road and Junction classes
│   ├── vehicle.py          # Vehicle state and physics
│   ├── stats.py            # Statistics and data collection
│   └── visualizer.py       # Matplotlib animation logic
├── main.py                 # Network definition and entry point
├── requirements.txt        # Python dependencies
└── .gitignore              # Git ignore rules
```

## Installation and Execution
Ensure Python 3.x is installed along with the necessary dependencies:

```bash
pip install -r requirements.txt
```

To execute the simulation and generate the statistical report and visualization:

```bash
python main.py
```

## Mathematical Modeling
The simulator supports two traffic generation models:

1. **Bernoulli Process:** A single vehicle has a fixed probability $p$ of spawning at each time step.
2. **Poisson Process:** The number of vehicles arriving at a source in a single time step follows a Poisson distribution. The probability of $k$ arrivals is given by:
   $$P(k) = \frac{\lambda^k e^{-\lambda}}{k!}$$
   where $\lambda$ is the arrival rate.

## Statistics and Metrics
The system collects and reports the following performance metrics:
* **Throughput:** Average number of vehicles successfully exiting the network per time step.
* **Average Total Travel Time:** The mean time taken for a vehicle to traverse from source to sink.
* **Delay Separation:** Breakdown of total time into Average Driving Time and Average Waiting Time (Queue Delay).
* **Link Utilization:** Percentage of the simulation duration each road segment spent at maximum capacity.
* **Peak Queue Length:** The maximum number of vehicles queued at each road segment.