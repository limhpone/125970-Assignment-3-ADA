# Empirical Analysis of Search Structures (ADA Ass3 Question 8)

Author: Aye Khin Khin Hpone (Yolanda Lim) - st125970

## Table of Contents

- [Empirical Analysis of Search Structures (ADA Ass3 Question 8)](#empirical-analysis-of-search-structures-ada-ass3-question-8)
  - [Table of Contents](#table-of-contents)
  - [1. Project Overview](#1-project-overview)
  - [2. Implementation Approach](#2-implementation-approach)
    - [2.1 Binary Search Tree](#21-binary-search-tree)
    - [2.2 Red-Black Tree](#22-red-black-tree)
    - [2.3 Hash Table](#23-hash-table)
  - [3. Experimental Setup](#3-experimental-setup)
  - [4. Dataset Design](#4-dataset-design)
    - [4.1 Random Input](#41-random-input)
    - [4.2 Sorted Input](#42-sorted-input)
    - [4.3 Adversarial Input](#43-adversarial-input)
  - [5. Results](#5-results)
    - [Insertion Time](#insertion-time)
    - [Successful Search Time](#successful-search-time)
    - [Unsuccessful Search Time](#unsuccessful-search-time)
    - [Full-Run Highlights (from `results/experiment_summary.csv`)](#full-run-highlights-from-resultsexperiment_summarycsv)
  - [6. Discussion](#6-discussion)
  - [7. Conclusion](#7-conclusion)
  - [8. How to Run](#8-how-to-run)

## 1. Project Overview

This project compares three search structures for ADA2026 Assignment 3 Question 8:

- Binary Search Tree
- Red-Black Tree
- Hash Table (separate chaining)

The program measures insertion and search performance under multiple input patterns and exports the results as CSV tables and plots.

Main files:

- `search_structures_yolanda.py`
- `results/` (full-mode artifacts)
- `results_quick/` (quick-mode artifacts)

## 2. Implementation Approach

### 2.1 Binary Search Tree

- Iterative `insert` and `search`
- No self-balancing
- Height measured by BFS after insertion
- Expected worst-case height approaches $n$ for ordered insertions.

### 2.2 Red-Black Tree

- Uses a `NIL` sentinel node
- Rebalancing through recoloring and rotations after insertion
- Iterative `search`
- Height is expected to stay $O(\log n)$.

### 2.3 Hash Table

- Separate chaining with list buckets
- Hash function: `key % table_size`
- Reports load factor, average non-empty chain length, and collision count
- Adversarial hash input is constructed to force bucket concentration

## 3. Experimental Setup

- Timer: `time.perf_counter()`
- Measures: insertion, successful search, unsuccessful search
- Output: console summary + CSV + PNG plots

Run modes:

- Full mode:
  - Sizes: `1000`, `10000`, `100000`
  - Trials: `3`
  - Search sample size: up to `1000` hits and `1000` misses
- Quick mode:
  - Sizes: `100`, `1000`
  - Trials: `2`
  - Search sample size: up to `100` hits and `100` misses

## 4. Dataset Design

### 4.1 Random Input

- Unique keys sampled from a wider numeric range
- Represents average-case behavior

### 4.2 Sorted Input

- Ascending insertion order
- Produces worst-case behavior for plain BST
- Red-Black Tree should remain balanced

### 4.3 Adversarial Input

- Trees use reverse-sorted insertion
- Hash table uses multiples of table size so keys collide strongly
- Highlights worst-case or near-worst-case degradation behavior.

## 5. Results

The script generates these full-mode evidence files:

- `results/experiment_summary.csv`
- `results/experiment_trials.csv`
- `results/insert_times.png`
- `results/search_hit_times.png`
- `results/search_miss_times.png`

### Insertion Time

![Insertion Time Plot](results/insert_times.png)

### Successful Search Time

![Successful Search Plot](results/search_hit_times.png)

### Unsuccessful Search Time

![Unsuccessful Search Plot](results/search_miss_times.png)

CSV evidence used for this report is in:

- `results/experiment_summary.csv`
- `results/experiment_trials.csv`

These CSV files are the raw measured data, and the plots above are visual summaries from the same run.

### Full-Run Highlights (from `results/experiment_summary.csv`)

At `n=100,000`:

- **Sorted pattern**
  - BST: insert `221.467 s`, hit search `2.384 s`, height `100000`
  - Red-Black Tree: insert `0.351 s`, hit search `0.001693 s`, height `31`
  - Hash Table: insert `0.016 s`, hit search `0.000298 s`, collisions `0`

- **Adversarial pattern** (BST reverse-sorted, hash all-same-bucket)
  - BST: insert `144.198 s`, miss search `3.405 s`, height `100000`
  - Red-Black Tree: insert `0.215 s`, miss search `0.001433 s`, height `31`
  - Hash Table: insert `28.499 s`, hit search `0.314 s`, collisions `99999`

- **Random pattern**
  - BST: height `40.67`
  - Red-Black Tree: height `20.00`
  - Hash Table: load factor `0.769`, average non-empty chain length `1.39`

Important for final submission:

- Before packaging your submission, run full mode once so `results/` contains assignment-scale evidence:

```powershell
python search_structures_yolanda.py --mode full
```

## 6. Discussion

The measured results match the expected complexity trends:

- **BST**: very sensitive to insertion order. With sorted or reverse-sorted data, tree height reaches `n`, causing very high insertion and search times.
- **Red-Black Tree**: remains balanced across all patterns (height around `31` at `n=100,000`), so insertion and search stay consistently low.
- **Hash Table**: excellent average performance on random/sorted distributions, but degrades strongly under forced-collision adversarial input.

This confirms that balancing (Red-Black Tree) improves worst-case behavior for tree-based search, while hash-table performance depends heavily on key distribution and collision behavior.

## 7. Conclusion

This empirical study confirms the expected behavior of the three data structures under average and worst-case inputs. The BST is highly sensitive to insertion order and becomes impractical at large `n` under sorted or reverse-sorted patterns, as shown by its extreme insertion/search times and height growth to `100000`. The Red-Black Tree maintains balanced height and consistently low operation times across all tested patterns, making it the most robust tree-based option for unpredictable inputs. The Hash Table provides the fastest average performance when key distribution is favorable, but adversarial collisions significantly degrade insertion and successful-search performance. Overall, the full-mode results in `results/experiment_summary.csv` and `results/experiment_trials.csv`, together with the generated plots, provide strong empirical evidence aligned with theoretical time-complexity analysis.

## 8. How to Run

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

1. Run a quick validation:

```powershell
python search_structures_yolanda.py --mode quick
```

1. Run the final assignment benchmark:

```powershell
python search_structures_yolanda.py --mode full
```

Notes:

- Quick mode writes to `results_quick/`
- Full mode writes to `results/`
- Full mode can take longer because BST worst-case insertion is intentional
