module perf
( 
	input	                clk, resetb,
	input					dinA, dinB,
	output reg				doutA, doutB
);  


always @(posedge clk or negedge resetb)
begin
	if(!resetb) begin
		doutA <= 'd0;
		doutB <= 'd0;
	end
	else begin
		doutA <= dinA;
		doutB <= dinA;
	end
end

endmodule

