import csv
import sys
import matplotlib.pyplot as plt

def load_spikes(path):
    timesteps, neuron_ids = [], []
    with open(path) as f:
        for row in csv.DictReader(f):
            timesteps.append(int(row["timestep"]))
            neuron_ids.append(int(row["neuron_id"]))
    return timesteps, neuron_ids

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/spikes.csv"
    timesteps, neuron_ids = load_spikes(path)
    plt.figure(figsize=(10, 4))
    plt.scatter(timesteps, neuron_ids, marker="|", s=100, color="black")
    plt.xlabel("Timestep")
    plt.ylabel("Neuron ID")
    plt.title("Spike raster")
    plt.tight_layout()
    plt.savefig("data/raster.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()