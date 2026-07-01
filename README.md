# 🚌 Public Transport Route Optimization Using Q-Learning

A Reinforcement Learning project that uses **Q-Learning** to determine the optimal route through a 25-stop public transport network while minimizing total journey time under dynamic conditions such as congestion, route closures, and varying traffic conditions.

---

## 🌐 Live Demo

**Streamlit App:**  
https://public-transport-route-optimization.streamlit.app/

---

## 📋 Table of Contents

- Overview
- Features
- Project Structure
- Architecture
- Installation
- Usage
- How It Works
- Configuration
- Screenshots
- License

---

## 📖 Overview

This project models a city's public transport network as a directed graph consisting of **25 stops** connected by **25 transport routes** spanning three transportation modes.

| Mode | Routes | Speed Range | Characteristics |
|------|--------|-------------|----------------|
| 🚌 Bus | 8 Routes | 15–28 km/h | Covers grid and diagonal roads |
| 🚇 Metro | 5 Routes | 55–72 km/h | Fast intercity corridors |
| 🛺 Auto | 12 Routes | 13–20 km/h | Short cross-links between rows |

The Q-Learning agent learns to navigate from a source stop to a destination while adapting to:

- Dynamic congestion
- Random route closures
- Peak and off-peak waiting times
- Transfer costs between transport modes

---

## ✨ Features

- Q-Learning based route optimization
- Dynamic congestion simulation
- Random route closures
- Peak / Off-Peak travel simulation
- Multi-modal transport network (Bus, Metro & Auto)
- Transfer between transport modes at hub stops
- Dijkstra shortest-path comparison
- Interactive Streamlit dashboard
- Network visualization
- Learning curve visualization
- Q-Table visualization
- Download trained Q-Table as CSV

---

## 📁 Project Structure

```
Public-Transport-Route-Optimization/
│
├── network.py
├── environment.py
├── mdp.py
├── agent.py
├── comparison.py
├── visualize.py
├── main.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🏗️ Architecture

The project is divided into multiple modules:

- **network.py** — Defines the transport network topology.
- **environment.py** — Simulates congestion, route closures, and travel conditions.
- **mdp.py** — Defines the Markov Decision Process.
- **agent.py** — Implements the Q-Learning algorithm.
- **comparison.py** — Computes the Dijkstra shortest path for benchmarking.
- **visualize.py** — Generates network and training visualizations.
- **app.py** — Streamlit dashboard.

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/kunjpatel6151/Public-Transport-Route-Optimization.git

cd Public-Transport-Route-Optimization
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## 🚀 Usage

1. Select source and destination stops.
2. Configure:
   - Episodes
   - Learning Rate (α)
   - Discount Factor (γ)
   - Exploration Rate (ε)
   - Closure Probability
   - Time Band
3. Click **Run & Find Optimal Path**.
4. Analyze:
   - Optimal route
   - Learning curve
   - Network visualization
   - Q-table
   - Journey statistics

---

## 🧠 How It Works

### Travel Time

```
actual_speed = base_speed / congestion_factor

travel_time = (length_km / actual_speed) × 60
```

### Q-Learning Update

```
Q(s,a) ← Q(s,a) + α[R + γ max Q(s',a') − Q(s,a)]
```

The reward function considers:

- Travel time
- Waiting time
- Transfer cost
- Route availability
- Destination reward

---

## ⚙️ Configuration

### Hyperparameters

| Parameter | Default |
|-----------|---------|
| Episodes | 2000 |
| Learning Rate (α) | 0.10 |
| Discount Factor (γ) | 0.90 |
| Initial ε | 1.00 |
| Closure Probability | 0.10 |

### Transport Modes

- 🚌 Bus
- 🚇 Metro
- 🛺 Auto

---

## 📸 Screenshots

The Streamlit dashboard displays:

- 📊 Training Summary
- 🗺️ Network Visualization
- 📈 Learning Curve
- 🔥 Q-Table Visualization
- 🏁 Optimal Path Table

---

## 🎯 Educational Purpose

This project demonstrates the practical application of **Reinforcement Learning (Q-Learning)** in solving dynamic route optimization problems within a multi-modal public transportation network.

---

## 📄 License

This project is developed for academic and educational purposes as part of a **B.Tech Computer Science & Engineering** curriculum.