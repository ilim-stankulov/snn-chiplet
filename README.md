# snn-chiplet

Splits a spiking neural network across two chiplets, measures the die-to-die energy cost, and finds the best neuron assignment to minimise it.

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

- Optimal partition reduces cross-die traffic by 55% vs the worst split
- D2D link costs 10× more energy per spike than an on-die connection
- Only 2 of 70 balanced splits achieve the minimum cut weight