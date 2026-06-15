`default_nettype none

module lif_neuron #(parameter THRESH = 8'sd64, SHIFT = 3) (
    input  wire clk, input  wire rst_n, input  wire ena,
    input  wire signed [7:0] current_in,
    output reg  spike, output reg signed [7:0] v_mem
);
    wire signed [7:0] leak = v_mem >>> SHIFT;
    wire signed [7:0] v_next = v_mem - leak + current_in;

    always @(posedge clk) begin
        if (!rst_n) begin
            v_mem <= 8'sd0;
            spike <= 1'b0;
        end else if (ena) begin
            if (spike) begin
                v_mem <= 8'sd0;
                spike <= 1'b0;
            end else if (v_next >= THRESH) begin
                v_mem <= 8'sd0;
                spike <= 1'b1;
            end else begin
                v_mem <= v_next;
                spike <= 1'b0;
            end
        end
    end
endmodule

module weight_storage (
    input  wire clk, input  wire rst_n, input  wire s_data, 
    input  wire s_clk_en, input  wire mode_prog,
    output reg  [127:0] weights, output wire prog_done
);
    reg [7:0] bit_cnt;
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
endmodule

module synapse_matrix (
    input  wire [7:0] all_spikes, input  wire [127:0] w,
    output wire signed [7:0] i0, output wire signed [7:0] i1, 
    output wire signed [7:0] i2, output wire signed [7:0] i3
);
    function signed [7:0] calc;
        input [7:0] s;
        input [31:0] weights;
        integer i;
        reg signed [7:0] sum;
        begin
            sum = 8'sd0;
            for (i = 0; i < 8; i = i + 1) begin
                if (s[i]) sum = sum + $signed(weights[i*4 +: 4]);
            end
            calc = sum;
        end
    endfunction

    assign i0 = calc(all_spikes, w[31:0]);
    assign i1 = calc(all_spikes, w[63:32]);
    assign i2 = calc(all_spikes, w[95:64]);
    assign i3 = calc(all_spikes, w[127:96]);
endmodule