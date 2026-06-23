`default_nettype none
`timescale 1ns / 1ps

module tb_system ();
    initial begin
        $dumpfile("tb_system.fst");
        $dumpvars(0, tb_system);
        #1;
    end

    reg clk, rst_n, ena;
    reg c0_s_data, c0_s_clk_en, c0_mode_prog;
    reg c1_s_data, c1_s_clk_en, c1_mode_prog;
    wire c0_prog_done, c1_prog_done;
    reg [3:0] c0_stimulus, c1_stimulus;
    wire [3:0] c0_spikes, c1_spikes;
    wire [31:0] c0_to_c1_energy, c1_to_c0_energy;
    wire [31:0] c0_to_c1_count, c1_to_c0_count;
    
    snn_system dut (
        .clk(clk), .rst_n(rst_n), .ena(ena),
        .c0_s_data(c0_s_data), .c0_s_clk_en(c0_s_clk_en), .c0_mode_prog(c0_mode_prog),
        .c0_prog_done(c0_prog_done),
        .c1_s_data(c1_s_data), .c1_s_clk_en(c1_s_clk_en), .c1_mode_prog(c1_mode_prog),
        .c1_prog_done(c1_prog_done),
        .c0_stimulus(c0_stimulus), .c1_stimulus(c1_stimulus),
        .c0_spikes(c0_spikes), .c1_spikes(c1_spikes),
        .c0_to_c1_energy(c0_to_c1_energy), .c1_to_c0_energy(c1_to_c0_energy),
        .c0_to_c1_count(c0_to_c1_count),   .c1_to_c0_count(c1_to_c0_count)
    );

endmodule
