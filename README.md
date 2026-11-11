# snn-chiplet

A toy model of splitting a spiking neural network across two chiplets: it estimates die-to-die traffic and energy for each possible neuron assignment and finds the split that minimises it.

## Background

Extends a 4-neuron LIF SNN (originally built for TinyTapeout) into an
8-neuron two-chiplet system. Each chiplet holds 4 neurons. They communicate
through a modelled die-to-die link that adds latency and charges energy per
spike. The goal is to find which neurons belong together on the same die.

## Structure

| Path | Description |
|------|-------------|
| `src/lif_components.v` | LIF neuron, synapse matrix, weight storage primitives |
| `src/snn_tile.v` | 4-neuron tile with 8-input synapse matrix |
| `src/d2d_link.v` | Die-to-die link model: latency pipeline + energy counters |
| `src/system_top.v` | Two-chiplet system with bidirectional D2D links |
| `test/test_system.py` | cocotb test: programs both chiplets, runs simulation, logs spikes |
| `analysis/energy_model.py` | Energy breakdown: ideal vs baseline cost |
| `analysis/partition.py` | Exhaustive search over all 70 balanced neuron splits |

## Running

**Single-chip baseline test:**
```bash
cd test && make
```

**Two-chiplet system simulation:**
```bash
cd test && make SYSTEM=yes
```

**Energy analysis:**
```bash
python3 analysis/energy_model.py
```

**Partition optimizer:**
```bash
python3 analysis/partition.py
```

## Results

On a hand-made 8-neuron network with two strongly connected groups of four:

- The best split cuts 64 units of cross-die connection weight, against 144 for the worst split.
  Because the network was built with two groups, the optimiser recovering them is a sanity check,
  not a discovery.
- The best split is unique up to swapping the two dies.