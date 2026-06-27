/*
 * Copyright (c) 2026 Ilim Stankulov
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module snn_tile #(parameter THRESH = 8'sd64, SHIFT = 3) (
    input  wire        clk, rst_n, ena,
    input  wire        s_data, s_clk_en, mode_prog,
    output wire        prog_done,
    input  wire [3:0]  remote_spikes,
    input  wire [3:0]  stimulus,
    output wire [3:0]  local_spikes
);

    reg  [127:0] weights;
    reg  [7:0]   bit_cnt;
    assign prog_done = (bit_cnt == 8'd128);

    always @(posedge clk) begin
        if (!rst_n) begin
            weights <= 128'b0;
            bit_cnt <= 8'b0;
        end else if (mode_prog && s_clk_en) begin
            weights <= {weights[126:0], s_data};
            if (bit_cnt < 128) bit_cnt <= bit_cnt + 1;
        end
    end

    wire [7:0] all_spikes = {remote_spikes, local_spikes | stimulus};

    wire signed [7:0] i0, i1, i2, i3;
    
    synapse_matrix sm (
        .all_spikes(all_spikes), .w(weights),
        .i0(i0), .i1(i1), .i2(i2), .i3(i3)
    );
    lif_neuron #(.THRESH(THRESH), .SHIFT(SHIFT)) n0 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .current_in(i0), .spike(local_spikes[0]), .v_mem()
    );
    lif_neuron #(.THRESH(THRESH), .SHIFT(SHIFT)) n1 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .current_in(i1), .spike(local_spikes[1]), .v_mem()
    );
    lif_neuron #(.THRESH(THRESH), .SHIFT(SHIFT)) n2 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .current_in(i2), .spike(local_spikes[2]), .v_mem()
    );
    lif_neuron #(.THRESH(THRESH), .SHIFT(SHIFT)) n3 (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .current_in(i3), .spike(local_spikes[3]), .v_mem()
    );

endmodule
