"""
ADA2026 Assignment 3 - Question 8
Empirical Analysis of Search Structures: BST, Red-Black Tree, Hash Table
"""

import time
import argparse
import csv
import random
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# 1. Binary Search Tree
# ─────────────────────────────────────────────

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = BSTNode(key)
                    return
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = BSTNode(key)
                    return
                node = node.right
            else:
                return  # duplicate

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False

    def height(self):
        if self.root is None:
            return 0
        # Iterative BFS height
        from collections import deque
        q = deque([(self.root, 1)])
        max_h = 0
        while q:
            node, h = q.popleft()
            max_h = max(max_h, h)
            if node.left:
                q.append((node.left, h + 1))
            if node.right:
                q.append((node.right, h + 1))
        return max_h


# ─────────────────────────────────────────────
# 2. Red-Black Tree
# ─────────────────────────────────────────────

RED = True
BLACK = False

class RBNode:
    def __init__(self, key):
        self.key = key
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(None)
        self.NIL.color = BLACK
        self.root = self.NIL

    def insert(self, key):
        z = RBNode(key)
        z.left = self.NIL
        z.right = self.NIL
        y = None
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            elif z.key > x.key:
                x = x.right
            else:
                return  # duplicate, skip
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.color = RED
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left if z.parent.parent else None:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left if z.parent.parent else self.NIL
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def search(self, key):
        x = self.root
        while x != self.NIL:
            if key == x.key:
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return False

    def height(self):
        if self.root == self.NIL:
            return 0
        from collections import deque
        q = deque([(self.root, 1)])
        max_h = 0
        while q:
            node, h = q.popleft()
            max_h = max(max_h, h)
            if node.left != self.NIL:
                q.append((node.left, h + 1))
            if node.right != self.NIL:
                q.append((node.right, h + 1))
        return max_h


# ─────────────────────────────────────────────
# 3. Hash Table with Separate Chaining
# ─────────────────────────────────────────────

class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        return key % self.size

    def insert(self, key):
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)
            self.count += 1

    def search(self, key):
        idx = self._hash(key)
        return key in self.buckets[idx]

    def load_factor(self):
        return self.count / self.size

    def avg_chain_length(self):
        non_empty = [b for b in self.buckets if b]
        return sum(len(b) for b in non_empty) / len(non_empty) if non_empty else 0

    def collision_count(self):
        return sum(len(b) - 1 for b in self.buckets if len(b) > 1)


# ─────────────────────────────────────────────
# 4. Dataset Generators
# ─────────────────────────────────────────────

BASE_OUTPUT_DIR = Path(__file__).resolve().parent
MODE_CONFIGS = {
    "quick": {
        "sizes": [100, 1_000],
        "trials": 2,
        "search_sample_size": 100,
        "output_dir": BASE_OUTPUT_DIR / "results_quick",
    },
    "full": {
        "sizes": [1_000, 10_000, 100_000],
        "trials": 3,
        "search_sample_size": 1_000,
        "output_dir": BASE_OUTPUT_DIR / "results",
    },
}


def random_input(n, rng):
    return rng.sample(range(n * 10), n)

def sorted_input(n):
    return list(range(1, n + 1))

def reverse_sorted_input(n):
    return list(range(n, 0, -1))

def adversarial_input_hash(n, table_size=101):
    """All keys map to same bucket: multiples of table_size."""
    return [table_size * i for i in range(1, n + 1)]


def make_search_miss_keys(count):
    return [-(index + 1) for index in range(count)]


def sample_search_hits(data, sample_size, rng):
    return rng.sample(data, min(sample_size, len(data)))


def build_pattern_case(pattern_name, n, rng, search_sample_size):
    ht_size = max(101, int(n * 1.3))

    if pattern_name == "Random":
        shared_data = random_input(n, rng)
        return {
            "label": "Random",
            "BST": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Red-Black Tree": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Hash Table": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {"size": ht_size},
            },
        }

    if pattern_name == "Sorted":
        shared_data = sorted_input(n)
        return {
            "label": "Sorted",
            "BST": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Red-Black Tree": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Hash Table": {
                "insert_keys": shared_data,
                "search_hits": sample_search_hits(shared_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {"size": ht_size},
            },
        }

    if pattern_name == "Adversarial":
        tree_data = reverse_sorted_input(n)
        hash_data = adversarial_input_hash(n, table_size=ht_size)
        return {
            "label": "Adversarial (BST=reverse-sorted, HT=all-same-bucket)",
            "BST": {
                "insert_keys": tree_data,
                "search_hits": sample_search_hits(tree_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Red-Black Tree": {
                "insert_keys": tree_data,
                "search_hits": sample_search_hits(tree_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {},
            },
            "Hash Table": {
                "insert_keys": hash_data,
                "search_hits": sample_search_hits(hash_data, search_sample_size, rng),
                "search_misses": make_search_miss_keys(min(search_sample_size, n)),
                "kwargs": {"size": ht_size},
            },
        }

    raise ValueError(f"Unsupported pattern: {pattern_name}")


# ─────────────────────────────────────────────
# 5. Benchmark Runner
# ─────────────────────────────────────────────

STRUCTURES = [
    ("BST", BinarySearchTree),
    ("Red-Black Tree", RedBlackTree),
    ("Hash Table", HashTable),
]


def benchmark_once(ds_class, insert_keys, search_hits, search_misses, ds_kwargs=None):
    if ds_kwargs is None:
        ds_kwargs = {}
    ds = ds_class(**ds_kwargs)

    # Insert
    t0 = time.perf_counter()
    for key in insert_keys:
        ds.insert(key)
    insert_time = time.perf_counter() - t0

    # Successful search
    t0 = time.perf_counter()
    for key in search_hits:
        ds.search(key)
    search_hit_time = time.perf_counter() - t0

    # Unsuccessful search
    t0 = time.perf_counter()
    for key in search_misses:
        ds.search(key)
    search_miss_time = time.perf_counter() - t0

    # Height (tree structures) or stats (hash)
    extra = {}
    if hasattr(ds, 'height'):
        extra['height'] = ds.height()
    if hasattr(ds, 'load_factor'):
        extra['load_factor'] = round(ds.load_factor(), 4)
        extra['avg_non_empty_chain_len'] = round(ds.avg_chain_length(), 4)
        extra['collisions'] = ds.collision_count()

    return {
        'insert_time': insert_time,
        'search_hit_time': search_hit_time,
        'search_miss_time': search_miss_time,
        'extra': extra,
    }


def summarize_metric(values):
    return statistics.mean(values), statistics.pstdev(values)


def summarize_trials(pattern_name, n, structure_name, trial_runs):
    insert_values = [run['insert_time'] for run in trial_runs]
    search_hit_values = [run['search_hit_time'] for run in trial_runs]
    search_miss_values = [run['search_miss_time'] for run in trial_runs]

    summary = {
        'pattern': pattern_name,
        'n': n,
        'structure': structure_name,
        'trials': len(trial_runs),
        'insert_mean_s': summarize_metric(insert_values)[0],
        'insert_std_s': summarize_metric(insert_values)[1],
        'search_hit_mean_s': summarize_metric(search_hit_values)[0],
        'search_hit_std_s': summarize_metric(search_hit_values)[1],
        'search_miss_mean_s': summarize_metric(search_miss_values)[0],
        'search_miss_std_s': summarize_metric(search_miss_values)[1],
    }

    all_extra_keys = sorted({key for run in trial_runs for key in run['extra']})
    for key in all_extra_keys:
        metric_values = [run['extra'][key] for run in trial_runs]
        summary[f'{key}_mean'] = statistics.mean(metric_values)

    return summary


def format_extra(summary_row):
    extras = []
    if 'height_mean' in summary_row:
        extras.append(f"height={summary_row['height_mean']:.2f}")
    if 'load_factor_mean' in summary_row:
        extras.append(f"load={summary_row['load_factor_mean']:.3f}")
    if 'avg_non_empty_chain_len_mean' in summary_row:
        extras.append(f"avg_chain={summary_row['avg_non_empty_chain_len_mean']:.2f}")
    if 'collisions_mean' in summary_row:
        extras.append(f"collisions={summary_row['collisions_mean']:.0f}")
    return '  '.join(extras)


def run_experiment(n, pattern_name, trials, rng, search_sample_size):
    display_label = build_pattern_case(pattern_name, n, rng, search_sample_size)['label']
    print(f"\n  n={n:,}  |  Pattern: {display_label}")
    print(
        f"  {'Structure':<18} {'Insert Avg(s)':>14} {'Hit Avg(s)':>12} {'Miss Avg(s)':>13} {'Extra':>30}"
    )
    print(f"  {'-'*95}")

    per_trial_rows = []
    summary_rows = []

    for structure_name, ds_class in STRUCTURES:
        trial_runs = []
        for trial in range(1, trials + 1):
            case_data = build_pattern_case(pattern_name, n, rng, search_sample_size)[structure_name]
            trial_result = benchmark_once(
                ds_class,
                case_data['insert_keys'],
                case_data['search_hits'],
                case_data['search_misses'],
                case_data['kwargs'],
            )
            trial_runs.append(trial_result)

            row = {
                'pattern': pattern_name,
                'pattern_label': display_label,
                'n': n,
                'structure': structure_name,
                'trial': trial,
                'insert_time_s': trial_result['insert_time'],
                'search_hit_time_s': trial_result['search_hit_time'],
                'search_miss_time_s': trial_result['search_miss_time'],
            }
            row.update(trial_result['extra'])
            per_trial_rows.append(row)

        summary_row = summarize_trials(pattern_name, n, structure_name, trial_runs)
        summary_row['pattern_label'] = display_label
        print(
            f"  {structure_name:<18}"
            f" {summary_row['insert_mean_s']:>14.6f}"
            f" {summary_row['search_hit_mean_s']:>12.6f}"
            f" {summary_row['search_miss_mean_s']:>13.6f}"
            f" {format_extra(summary_row):>30}"
        )
        summary_rows.append(summary_row)

    return per_trial_rows, summary_rows


def write_csv(path, rows, fieldnames):
    with path.open('w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_results(per_trial_rows, summary_rows, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    per_trial_fields = [
        'pattern',
        'pattern_label',
        'n',
        'structure',
        'trial',
        'insert_time_s',
        'search_hit_time_s',
        'search_miss_time_s',
        'height',
        'load_factor',
        'avg_non_empty_chain_len',
        'collisions',
    ]
    summary_fields = [
        'pattern',
        'pattern_label',
        'n',
        'structure',
        'trials',
        'insert_mean_s',
        'insert_std_s',
        'search_hit_mean_s',
        'search_hit_std_s',
        'search_miss_mean_s',
        'search_miss_std_s',
        'height_mean',
        'load_factor_mean',
        'avg_non_empty_chain_len_mean',
        'collisions_mean',
    ]

    normalized_trial_rows = []
    for row in per_trial_rows:
        normalized_trial_rows.append({field: row.get(field, '') for field in per_trial_fields})

    normalized_summary_rows = []
    for row in summary_rows:
        normalized_summary_rows.append({field: row.get(field, '') for field in summary_fields})

    write_csv(output_dir / 'experiment_trials.csv', normalized_trial_rows, per_trial_fields)
    write_csv(output_dir / 'experiment_summary.csv', normalized_summary_rows, summary_fields)


def save_metric_plot(summary_rows, metric_key, ylabel, filename, output_dir):
    patterns = ['Random', 'Sorted', 'Adversarial']
    fig, axes = plt.subplots(1, len(patterns), figsize=(18, 5), sharey=True)

    for axis, pattern_name in zip(axes, patterns):
        pattern_rows = [row for row in summary_rows if row['pattern'] == pattern_name]
        for structure_name, _ in STRUCTURES:
            structure_rows = sorted(
                [row for row in pattern_rows if row['structure'] == structure_name],
                key=lambda row: row['n'],
            )
            axis.plot(
                [row['n'] for row in structure_rows],
                [row[metric_key] for row in structure_rows],
                marker='o',
                linewidth=2,
                label=structure_name,
            )

        axis.set_title(pattern_name)
        axis.set_xscale('log')
        axis.set_xlabel('Dataset size (n)')
        axis.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

    axes[0].set_ylabel(ylabel)
    axes[-1].legend(loc='best')
    fig.suptitle(f'{ylabel} by Structure and Input Pattern')
    fig.tight_layout()
    fig.savefig(output_dir / filename, dpi=200, bbox_inches='tight')
    plt.close(fig)


def create_plots(summary_rows, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    save_metric_plot(summary_rows, 'insert_mean_s', 'Insertion time (s)', 'insert_times.png', output_dir)
    save_metric_plot(summary_rows, 'search_hit_mean_s', 'Successful search time (s)', 'search_hit_times.png', output_dir)
    save_metric_plot(summary_rows, 'search_miss_mean_s', 'Unsuccessful search time (s)', 'search_miss_times.png', output_dir)


def parse_args():
    parser = argparse.ArgumentParser(description='Empirical analysis of search structures.')
    parser.add_argument(
        '--mode',
        choices=sorted(MODE_CONFIGS),
        default='full',
        help='Run quick validation benchmarks or the full assignment-scale experiment.',
    )
    return parser.parse_args()


# ─────────────────────────────────────────────
# 6. Main
# ─────────────────────────────────────────────

def main(mode='full'):
    config = MODE_CONFIGS[mode]
    rng = random.Random(2026)
    per_trial_rows = []
    summary_rows = []
    output_dir = config['output_dir']

    print("=" * 74)
    print("  ADA2026 - Assignment 3 Q8: Empirical Analysis of Search Structures")
    print("=" * 74)
    print(f"  Mode: {mode}")
    print(f"  Output directory: {output_dir.name}")

    for n in config['sizes']:
        print(f"\n{'━'*74}")
        print(f"  Dataset Size: n = {n:,}")
        print(f"{'━'*74}")

        for pattern_name in ["Random", "Sorted", "Adversarial"]:
            trial_rows, pattern_summary_rows = run_experiment(
                n,
                pattern_name,
                config['trials'],
                rng,
                config['search_sample_size'],
            )
            per_trial_rows.extend(trial_rows)
            summary_rows.extend(pattern_summary_rows)

    export_results(per_trial_rows, summary_rows, output_dir)
    create_plots(summary_rows, output_dir)

    print(f"\n{'='*74}")
    print("  Summary: Theoretical vs Empirical")
    print(f"{'='*74}")
    print("""
  STRUCTURE        OPERATION      RANDOM         SORTED         ADVERSARIAL
  ──────────────────────────────────────────────────────────────────────────
  BST              Insert         O(log n)       O(n)           O(n)
                   Search         O(log n)       O(n)           O(n)
                   Height         near log n     near n         near n

  Red-Black Tree   Insert         O(log n)       O(log n)       O(log n)
                   Search         O(log n)       O(log n)       O(log n)
                   Height         O(log n)       O(log n)       O(log n)

  Hash Table       Insert         O(1) avg       O(1) avg       O(n) worst
                   Search         O(1) avg       O(1) avg       O(n) worst
                   Collisions     low            low            concentrated
  ──────────────────────────────────────────────────────────────────────────
    Output files written to the selected output directory:
    - experiment_trials.csv
    - experiment_summary.csv
    - insert_times.png
    - search_hit_times.png
    - search_miss_times.png
    """)


if __name__ == "__main__":
    args = parse_args()
    main(args.mode)
