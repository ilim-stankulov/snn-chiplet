/*
 * Copyright (c) 2026 Ilim Stankulov
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_lif_snn (
    input  wire [7:0] ui_in,    // dedicated inputs
    output wire [7:0] uo_out,   // dedicated outputs
    input  wire [7:0] uio_in,   // bidirectional IOs — input path
    output wire [7:0] uio_out,  // bidirectional IOs — output path
    output wire [7:0] uio_oe,   // IO direction: 1=output, 0=input
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset — active low
);

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire [3:0] spikes;
    wire prog_done;

    wire [127:0] weights;

    weight_storage ws (
        .clk      (clk),
        .rst_n    (rst_n),
        .s_data   (ui_in[0]),
        .s_clk_en (ui_in[1]),
        .mode_prog(ui_in[2]),
        .weights  (weights),
        .prog_done(prog_done)
    );

    wire [7:0] all_spikes = {4'b0000, spikes};
    wire signed [7:0] i0, i1, i2, i3;

    synapse_matrix sm (
        .all_spikes(all_spikes),
        .w         (weights),
        .i0        (i0),
        .i1        (i1),
        .i2        (i2),
        .i3        (i3)
    );

    lif_neuron neuron0 (
        .clk       (clk),
        .rst_n     (rst_n),
        .ena       (ena),
        .current_in(i0),
        .spike     (spikes[0]),
        .v_mem     ()
    );

    lif_neuron neuron1 (
        .clk       (clk),
        .rst_n     (rst_n),
        .ena       (ena),
        .current_in(i1),
        .spike     (spikes[1]),
        .v_mem     ()
    );

    lif_neuron neuron2 (
        .clk       (clk),
        .rst_n     (rst_n),
        .ena       (ena),
        .current_in(i2),
        .spike     (spikes[2]),
        .v_mem     ()
    );

    lif_neuron neuron3 (
        .clk       (clk),
        .rst_n     (rst_n),
        .ena       (ena),
        .current_in(i3),
        .spike     (spikes[3]),
        .v_mem     ()
    );

    assign uo_out = {3'b000, prog_done, spikes};

endmodule
