/*
 * Copyright (c) 2026 Ilim Stankulov
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module d2d_link #(parameter LATENCY = 4, parameter integer E_PER_SPIKE = 10, parameter DATA_W = 4)(
    input  wire              clk, rst_n,
    input  wire [DATA_W-1:0] tx_spikes,
    output wire [DATA_W-1:0] rx_spikes,
    output reg  [31:0]       energy_count,
    output reg  [31:0]       spike_count
);

    reg [DATA_W-1:0] pipe [0:LATENCY-1];
    assign rx_spikes = pipe[LATENCY-1];

    wire [2:0] tx_pop = tx_spikes[0] + tx_spikes[1] + tx_spikes[2] + tx_spikes[3];

    integer i;
    always @(posedge clk) begin
        if (!rst_n) begin
            for (i = 0; i < LATENCY; i = i + 1)
                pipe[i] <= {DATA_W{1'b0}};
            energy_count <= 32'b0;
            spike_count  <= 32'b0;
        end else begin
            pipe[0] <= tx_spikes;
            for (i = 1; i < LATENCY; i = i + 1)
                pipe[i] <= pipe[i-1];
            if (|tx_spikes) begin
                energy_count <= energy_count + tx_pop * E_PER_SPIKE;
                spike_count  <= spike_count  + tx_pop;
            end
        end
    end
endmodule
