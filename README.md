# tmmc
An algorithm-based mathematical model

**Here is the given Problem-Statement**

# Aegis Protocol: The Online Disk Defense 🛡️

This repository contains the algorithmic solution and mathematical model for the **Tryst Mathematical Modelling Challenge (TMMC)**, hosted by MathSoc, IIT Delhi.

## 📝 Problem Overview
The "Aegis Protocol" is an interactive mathematical modelling and algorithmic programming problem. As the lead strategist for the planetary defense system, the objective is to defend against an unknown sequence of spatial energy anomalies (perfectly circular disks) using a fixed grid of defense laser satellites. 

* **Satellites:** The exact 2D coordinates of all $N$ satellites are known at the start of the simulation.
* **Anomalies:** Disks arrive one at a time sequentially, with absolutely zero knowledge of future anomalies.
* **Defense Rules:** Every anomaly must be intersected by at least one active satellite. Once powered on, a satellite remains active forever.
* **Objective:** Minimize the total number of powered-on satellites by the end of the simulation (energy is strictly limited).

## 📐 Mathematical Formulation
* Let $P \subset \mathbb{R}^2$ be a set of $N$ points (available satellites).
* Let $\mathcal{C} = \{D_1, D_2, ..., D_Q\}$ be the sequence of $Q$ disks (anomalies).
* Each disk $D_i$ has center coordinates $(C_{x,i}, C_{y,i})$ and radius $R_i$.
* We maintain an active "hitting set" $H_i \subseteq P$ ensuring $H_i \subseteq H_{i+1}$.
* For every arrived disk $D_j$ ($1 \le j \le i$), $D_j \cap H_i \neq \emptyset$.
* **Optimization Goal:** Minimize the final size of the hitting set, $|H_Q|$.

## ⚙️ Interactive Protocol
The solution communicates with the judging system in real-time via standard input/output (flushing outputs is required).

1. **Phase 1 (Initialization):** The system reads the total number of satellites ($N$) and their respective $x, y$ coordinates.
2. **Phase 2 (Online Queries):** The system reads the total number of anomalies ($Q$). For each query, it reads the center and radius ($C_x, C_y, R$) of the new anomaly and outputs the index ($S_{idx}$) of the satellite chosen to intersect it. Outputting an already-active satellite costs nothing extra.

## 🚀 Constraints
* $1 \le N \le 10^5$
* $1 \le Q \le 10^4$
* $-10^6 \le x_k, y_k, C_x, C_y \le 10^6$
* $1.0 \le R \le 100.0$
* *Guarantee:* There is always at least one point in $P$ strictly inside or on the boundary of every given disk.

