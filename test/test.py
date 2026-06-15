# SPDX-FileCopyrightText: © 2026 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles


async def shift_bit(dut, bit):
    current = int(dut.ui_in.value)
    dut.ui_in.value = (current & ~0b011) | (bit & 1) | (1 << 1)
    await RisingEdge(dut.clk)
    current = int(dut.ui_in.value)
    dut.ui_in.value = current & ~(1 << 1)
    await RisingEdge(dut.clk)


async def program_weights(dut, pattern):
    dut.ui_in.value = 0b100
    await RisingEdge(dut.clk)
    for i in range(127, -1, -1):
        bit = (pattern >> i) & 1
        await shift_bit(dut, bit)
    dut.ui_in.value = 0b000
    await RisingEdge(dut.clk)


# TEST 1 - reset clears everything
@cocotb.test()
async def test_reset(dut):
    dut._log.info("Test 1 — reset")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value  = 1
    dut.ena.value    = 1
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)

    assert dut.uo_out.value == 0, \
        f"expected uo_out=0 after reset, got {dut.uo_out.value}"

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
    dut._log.info("PASS")


# TEST 2 - weight programming sets prog_done
@cocotb.test()
async def test_weight_programming(dut):
    dut._log.info("Test 2 — weight programming")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value  = 0
    dut.ena.value    = 0
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    assert (int(dut.uo_out.value) >> 4) & 1 == 0, \
        "prog_done should be 0 before loading weights"

    weight_pattern = int("0101" * 32, 2)
    await program_weights(dut, weight_pattern)
    await ClockCycles(dut.clk, 2)

    assert (int(dut.uo_out.value) >> 4) & 1 == 1, \
        "prog_done should be 1 after loading 128 bits"

    dut._log.info("PASS")


# TEST 3 - prog_done clears on mode switching
@cocotb.test()
async def test_prog_done_clears(dut):
    dut._log.info("Test 3 — prog_done clears on reset")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value  = 0
    dut.ena.value    = 0
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    weight_pattern = int("0101" * 32, 2)
    await program_weights(dut, weight_pattern)
    await ClockCycles(dut.clk, 2)

    assert (int(dut.uo_out.value) >> 4) & 1 == 1, \
        "expected prog_done=1 after programming"

    # reset should clear prog_done
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    assert (int(dut.uo_out.value) >> 4) & 1 == 0, \
        "prog_done should clear on reset"

    dut.rst_n.value = 1
    dut._log.info("PASS")


# TEST 4 - no spikes with zero weights
@cocotb.test()
async def test_no_spikes_zero_weights(dut):
    dut._log.info("Test 4 — no spikes with zero weights")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value  = 0
    dut.ena.value    = 0
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    await program_weights(dut, 0)
    await ClockCycles(dut.clk, 2)

    dut.ena.value = 1
    await ClockCycles(dut.clk, 200)

    spike_bits = int(dut.uo_out.value) & 0b1111
    assert spike_bits == 0, \
        f"expected no spikes with zero weights, got {spike_bits}"

    dut._log.info("PASS")


# TEST 5 - outputs do not go undefined
@cocotb.test()
async def test_outputs_always_valid(dut):
    dut._log.info("Test 5 — outputs stay valid for 500 cycles")
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst_n.value  = 0
    dut.ena.value    = 0
    dut.ui_in.value  = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    weight_pattern = int("0111" * 32, 2)
    await program_weights(dut, weight_pattern)
    await ClockCycles(dut.clk, 2)

    dut.ena.value = 1
    for _ in range(500):
        await RisingEdge(dut.clk)
        assert dut.uo_out.value.is_resolvable, \
            "output contains X or Z — something is undriven"

    dut._log.info("PASS")