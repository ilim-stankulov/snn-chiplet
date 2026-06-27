# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Ilim Stankulov

import csv
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

WEIGHT_BLOCK   = 0x33337777
WEIGHT_PATTERN = (WEIGHT_BLOCK << 96) | (WEIGHT_BLOCK << 64) | \
                 (WEIGHT_BLOCK << 32) |  WEIGHT_BLOCK

E_PER_SPIKE_ONDIE = 1
E_PER_SPIKE_D2D   = 10

async def program_tile(dut, s_data, s_clk_en, mode_prog, pattern):
    mode_prog.value = 1
    await RisingEdge(dut.clk)
    for i in range(127, -1, -1):
        bit = (pattern >> i) & 1
        s_data.value   = bit
        s_clk_en.value = 1
        await RisingEdge(dut.clk)
        s_clk_en.value = 0
        await RisingEdge(dut.clk)
    mode_prog.value = 0
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_two_chiplet_energy(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value = 0
    dut.ena.value   = 0
    dut.c0_stimulus.value = 0
    dut.c1_stimulus.value = 0
    for sig in (dut.c0_s_data, dut.c0_s_clk_en, dut.c0_mode_prog,
                dut.c1_s_data, dut.c1_s_clk_en, dut.c1_mode_prog):
        sig.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    await program_tile(dut, dut.c0_s_data, dut.c0_s_clk_en, dut.c0_mode_prog, WEIGHT_PATTERN)
    await program_tile(dut, dut.c1_s_data, dut.c1_s_clk_en, dut.c1_mode_prog, WEIGHT_PATTERN)
    await ClockCycles(dut.clk, 2)

    assert int(dut.c0_prog_done.value) == 1, "chiplet 0 weight programming failed"
    assert int(dut.c1_prog_done.value) == 1, "chiplet 1 weight programming failed"

    dut.ena.value         = 1

    spike_log = []
    for t in range(1000):
        dut.c0_stimulus.value = 0xF if t % 20 < 3 else 0
        dut.c1_stimulus.value = 0xF if t % 20 < 3 else 0

        await RisingEdge(dut.clk)
        c0 = int(dut.c0_spikes.value)
        c1 = int(dut.c1_spikes.value)
        for nid in range(4):
            if (c0 >> nid) & 1:
                spike_log.append((t, nid,     0))
            if (c1 >> nid) & 1:
                spike_log.append((t, nid + 4, 1))

    with open("../data/spikes_system.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["timestep", "neuron_id", "chiplet_id"])
        w.writeheader()
        for ts, nid, cid in spike_log:
            w.writerow({"timestep": ts, "neuron_id": nid, "chiplet_id": cid})

    e_0to1 = int(dut.c0_to_c1_energy.value)
    e_1to0 = int(dut.c1_to_c0_energy.value)
    n_0to1 = int(dut.c0_to_c1_count.value)
    n_1to0 = int(dut.c1_to_c0_count.value)

    total_spikes = len(spike_log)
    cross_spikes = n_0to1 + n_1to0
    ondie_spikes = total_spikes - cross_spikes

    dut._log.info(f"Total spikes:     {total_spikes}")
    dut._log.info(f"Cross-die spikes: {cross_spikes} ({100*cross_spikes/max(total_spikes,1):.1f}%)")
    dut._log.info(f"On-die energy:    {ondie_spikes  * E_PER_SPIKE_ONDIE} units")
    dut._log.info(f"D2D energy:       {e_0to1 + e_1to0} units")

    assert total_spikes > 0, "network produced no spikes — check weight programming"
