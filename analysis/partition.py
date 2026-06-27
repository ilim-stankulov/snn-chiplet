import sys
import itertools
import numpy as np
import matplotlib.pyplot as plt

def cut_weight(W, partition_A):
    A = set(partition_A)
    B = set(range(8)) - A
    cost = 0
    for i in A:
        for j in B:
            cost += abs(W[i][j]) + abs(W[j][i])
    return cost

def default_weights():
    W = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if i == j:
                continue
            W[i][j] = 7 if (i < 4) == (j < 4) else 2
    return W

def main():
    if len(sys.argv) > 1:
        W = np.loadtxt(sys.argv[1], delimiter=",")
    else:
        W = default_weights()
        print("Using built-in example weight matrix.")

    neurons = list(range(8))
    results = []
    for combo in itertools.combinations(neurons, 4):
        cost = cut_weight(W, combo)
        results.append((cost, sorted(combo), sorted(set(neurons) - set(combo))))
    results.sort()

    print(f"\n{'Rank':<6} {'Cut weight':<14} {'Chiplet 0':<20} {'Chiplet 1'}")
    print("-" * 60)
    for rank, (cost, A, B) in enumerate(results[:10], 1):
        print(f"{rank:<6} {cost:<14.1f} {str(A):<20} {B}")

    best_cost,  best_A,  best_B  = results[0]
    worst_cost = results[-1][0]
    print(f"\nOptimal split:  {best_A} | {best_B}  (cut = {best_cost:.1f})")
    print(f"Worst split:    cut = {worst_cost:.1f}")
    print(f"Savings vs worst: {worst_cost - best_cost:.1f} units "
          f"({100*(worst_cost - best_cost)/max(worst_cost,1):.1f}%)")

    import os
    _DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

    costs = [r[0] for r in results]
    plt.figure(figsize=(7, 4))
    plt.hist(costs, bins=20, color="steelblue", edgecolor="white")
    plt.axvline(best_cost,  color="green",  linestyle="--",
                label=f"optimal ({best_cost:.0f})")
    plt.axvline(worst_cost, color="tomato", linestyle="--",
                label=f"worst ({worst_cost:.0f})")
    plt.xlabel("Cut weight")
    plt.ylabel("Number of splits")
    plt.title("All 70 balanced splits ranked by cross-die communication cost")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(_DATA, "partition_costs.png"), dpi=150)
    plt.show()

if __name__ == "__main__":
    main()
