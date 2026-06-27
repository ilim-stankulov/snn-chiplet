/*
 * Copyright (c) 2026 Ilim Stankulov
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module snn_system #(parameter THRESH = 8'sd64, SHIFT = 3, D2D_LATENCY = 4, parameter integer E_PER_SPIKE = 10)(
    input  wire        clk, rst_n, ena,
    input  wire        c0_s_data, c0_s_clk_en, c0_mode_prog,
    output wire        c0_prog_done,
    input  wire        c1_s_data, c1_s_clk_en, c1_mode_prog,
    output wire        c1_prog_done,
    input  wire [3:0]  c0_stimulus, c1_stimulus,
    output wire [3:0]  c0_spikes,   c1_spikes,
    output wire [31:0] c0_to_c1_energy, c1_to_c0_energy,
    output wire [31:0] c0_to_c1_count,  c1_to_c0_count
);

    wire [3:0] c0_remote, c1_remote;

    snn_tile #(.THRESH(THRESH), .SHIFT(SHIFT)) chiplet0 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .s_data(c0_s_data), .s_clk_en(c0_s_clk_en), .mode_prog(c0_mode_prog),
        .prog_done(c0_prog_done),
        .remote_spikes(c0_remote),
        .stimulus(c0_stimulus),
        .local_spikes(c0_spikes)
    );

    snn_tile #(.THRESH(THRESH), .SHIFT(SHIFT)) chiplet1 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .s_data(c1_s_data), .s_clk_en(c1_s_clk_en), .mode_prog(c1_mode_prog),
        .prog_done(c1_prog_done),
        .remote_spikes(c1_remote),
        .stimulus(c1_stimulus),
        .local_spikes(c1_spikes)
    );
    
    d2d_link #(.LATENCY(D2D_LATENCY), .E_PER_SPIKE(E_PER_SPIKE)) link_0to1 (
        .clk(clk), .rst_n(rst_n),
        .tx_spikes(c0_spikes),
        .rx_spikes(c1_remote),
        .energy_count(c0_to_c1_energy),
        .spike_count(c0_to_c1_count)
    );

    d2d_link #(.LATENCY(D2D_LATENCY), .E_PER_SPIKE(E_PER_SPIKE)) link_1to0 (
        .clk(clk), .rst_n(rst_n),
        .tx_spikes(c1_spikes),
        .rx_spikes(c0_remote),
        .energy_count(c1_to_c0_energy),
        .spike_count(c1_to_c0_count)
    );

endmodule
