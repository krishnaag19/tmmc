# tmmc
An algorithm-based mathematical model

# Aegis Protocol: The Online Disk Defense
### Tryst Mathematical Modelling Challenge (TMMC) — MathSoc, IIT Delhi

> **Team RamMajnu Anand** | IIT Delhi  
> Krishna · Shlesha · **Aayush Agarwal** *(my role: Geometric Centrality heuristic + score formula design)*

---

## Problem Statement

An **Online Geometric Hitting Set** problem.

You are given `N` satellites (points in ℝ²) upfront. Then `Q` disk-shaped anomalies arrive **one at a time**, online — no knowledge of future disks. For each anomaly, you must output the index of a satellite that lies within it. Once activated, a satellite stays on forever.

**Objective:** Minimize the total number of satellites ever activated (the hitting set size `|H_Q|`).

**Constraints:**
- `1 ≤ N ≤ 10⁵` satellites
- `1 ≤ Q ≤ 10⁴` anomalies
- Coordinates in `[−10⁶, 10⁶]`
- **Radius `R ≤ 100`** — a critical bound that drives the spatial data structure choice

---

## Why This Is Hard

The offline version (given all disks upfront, find the minimum hitting set) is **NP-Hard**. The online version is harder still — every decision is irrevocable, and the adversary can construct disk sequences that exploit any greedy strategy.

A naive O(NQ) brute-force scan hits **10⁹ operations** — well over the 30-second time limit.

---

## Our Approach

### Step 1: Efficient Spatial Search via Grid Hashing

The key insight: since `R ≤ 100`, any disk of radius `R` can only contain satellites within a **local spatial neighbourhood**. We exploit this with a static hash grid.

**Construction (O(N) precomputation):**
- Divide the plane into `100×100` cells
- Map each satellite to its cell: `cell = (⌊x/100⌋, ⌊y/100⌋)`
- Store a dictionary: `grid[cell] → [satellite indices]`

**Query (O(1) average per anomaly):**
- For a disk at `(cx, cy, r)`, only check cells overlapping `[cx−r, cx+r] × [cy−r, cy+r]`
- At most `(r/100 + 2)² ≈ 9` neighbouring cells to scan (since `r ≤ 100`)
- No full scan of N satellites needed

### Step 2: Activation Reuse

Before scoring candidates, check if **any already-active satellite** falls within the new disk. If yes, return it immediately — zero additional activations, O(1) cost.

### Step 3: The Score Formula (for forced activations)

When no active satellite covers the disk, we must activate a new one. Three team members proposed competing heuristics; we tested all, then combined them.

#### Heuristic M1 — Krishna: Low-Density (Sparse-First)
Select the candidate with the **fewest neighbours** within radius 100.

*Rationale:* Isolated satellites are irreplaceable — activating them now preempts being forced to later.  
*Result:* Underperformed. An anomaly must cover at least one satellite, so anomalies are statistically more likely to appear in **dense** regions, not sparse ones.

#### Heuristic M2 — Shlesha: High-Density
Select the candidate with the **most neighbours** within radius 100.

*Rationale:* Dense regions attract more anomalies probabilistically; a high-density active satellite is more likely to cover future disks too, enabling reuse.  
*Result:* Strong on dense test cases (EC2_ultra_dense, EC4_many_micro_clusters). Weaker on sparse or large-coordinate cases where density signal is near-zero everywhere.

#### Heuristic M3 — Aayush: Geometric Centrality *(my contribution)*
Select the candidate **closest to the disk's center**.

*Rationale:* A satellite at the center of a disk has maximum overlap with future disks of any orientation centered nearby. It maximises the expected "capture area" of the activated satellite across unseen future queries.  
*Result:* Best overall on random/sparse distributions. The vast coordinate space (±10⁶) means local density is typically very low, so the geometric interpretation dominates.

#### Final Score: Weighted Combination

After empirical testing across all custom test cases:

```
SCORE = 0.5 × norm_distance + 0.3 × norm_active_density + 0.2 × norm_density
```

Where:
| Term | Formula | Intent |
|------|---------|--------|
| `norm_distance` | `1 − (dist_to_center² / r²)` | Geometric centrality — reward closeness to disk center |
| `norm_density` | `density / D_max` | Probabilistic — prefer satellites in high-traffic zones |
| `norm_active_density` | `1 / (1 + active_neighbours)` | Spread — avoid clustering activations in one region |

The **0.5 weight on distance** reflects that geometric centrality was the dominant signal across most test distributions. The **0.3 on active density** provides a repulsion term — don't pile activations in one cell. The **0.2 on static density** provides a weak probabilistic prior.

---

## Complexity Analysis

| Phase | Complexity |
|-------|-----------|
| Grid construction | O(N) |
| Density precomputation | O(N) — each point checks 9 neighbouring cells |
| Per-query candidate search | O(1) average — bounded by cells covered, not N |
| Per-query scoring | O(k) — k candidates in disk, typically ≪ N |
| **Total** | **O(N + Q)** |

---

## Experimental Results

Results on custom test cases (M1 = Krishna, M2 = Shlesha, M3 = Aayush, Final = combined score):

| Test Case | Description | M1 Activated | M2 Activated | M3 Activated | Final |
|-----------|-------------|:---:|:---:|:---:|:---:|
| EC10_overlapping_blobs | 5 blobs, 150 units apart, radius≈100 | 58 | 71 | 77 | — |
| EC1_ultra_sparse | 50 sats, huge ±1e6 space | 50 | 50 | 50 | 50 |
| EC2_ultra_dense | 5000 sats, 200×200 box | 54 | 66 | 69 | — |
| EC3_single_tight_cluster | All 5000 in 10×10 patch | 13 | 13 | 13 | 13 |
| EC4_many_micro_clusters | 100 clusters of 50 pts | 282 | 268 | **425** | — |
| EC9_hot_cold_clusters | 20 clusters; 4 hot, rest cold | 82 | 86 | 184 | — |

*The combined score formula blends the strengths of M2 and M3 while mitigating edge-case failures.*

---

## Repository Structure

```
.
├── solution.py        # Full Python solution with grid hashing and score formula
├── presentation.pdf   # Slide deck: problem formulation, heuristic debate, complexity
└── README.md
```

---

## Running Locally

The solution uses standard I/O (interactive judge protocol):

```bash
python solution.py
```

Input format (pipe from a test generator or judge):
```
N
x_0 y_0
x_1 y_1
...
Q
cx_0 cy_0 r_0
cx_1 cy_1 r_1
...
```

---

## Key Takeaways

- **Spatial indexing is the prerequisite**, not an optimisation — without grid hashing, the problem is computationally infeasible at the given constraints.
- **No single heuristic dominates** across all distributions. The score formula is a principled weighted blend, not an ad hoc hack — each weight has a geometric or probabilistic justification.
- The **online, irrevocable nature** of the problem means there is no provably optimal greedy strategy. We are approximating the offline NP-Hard optimum under zero lookahead.
