import csv
import sys
import matplotlib.pyplot as plt
import os
_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

E_ONDIE = 1
E_D2D   = 10

def load_spikes(path):
    c0_count = 0
    c1_count = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            if int(row["chiplet_id"]) == 0:
                c0_count += 1
            else:
                c1_count += 1
    return c0_count, c1_count

def compute_energy(c0_count, c1_count):
    total   = c0_count + c1_count
    # Worst case: no partitioning, every spike crosses the link
    d2d     = total * E_D2D
    # Best case: perfect partitioning, no spike ever crosses
    ondie   = total * E_ONDIE
    # Actual: everything crosses (our current baseline)
    actual_d2d   = total * E_D2D
    actual_ondie = 0
    return ondie, d2d, actual_ondie, actual_d2d

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_DATA, "spikes_system.csv")
    c0, c1 = load_spikes(path)
    total = c0 + c1

    print(f"Chiplet 0 spikes: {c0}")
    print(f"Chiplet 1 spikes: {c1}")
    print(f"Total spikes:     {total}")
    print(f"On-die energy (ideal):    {total * E_ONDIE} units")
    print(f"D2D energy (baseline):    {total * E_D2D} units")
    print(f"D2D overhead factor:      {E_D2D}x")

    categories = ["Ideal\n(perfect partition)", "Baseline\n(no partition)"]
    values     = [total * E_ONDIE, total * E_D2D]
    colors     = ["steelblue", "tomato"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories, values, color=colors, width=0.4)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 5,
                str(val), ha="center", va="bottom", fontsize=11)
    ax.set_ylabel("Energy (relative units)")
    ax.set_title("SNN chiplet energy: ideal vs baseline")
    plt.tight_layout()
    plt.savefig(os.path.join(_DATA, "energy_breakdown.png"), dpi=150)
    plt.show()

if __name__ == "__main__":
    main()
