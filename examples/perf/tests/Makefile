
TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
WPWD=$(shell pwd)
COCOCOMMON := $(WPWD)/../../cococommon

COCOTB_HDL_TIMEPRECISION = 1us
COCOTB_HDL_TIMEUNIT = 1us
export COCOTB_REDUCED_LOG_FMT=1
export COCOTB_ANSI_OUTPUT=1

VERILOG_SOURCES = ../hdl/perf.sv

TOPLEVEL := perf
MODULE   := $(TOPLEVEL)_cocotb

include $(shell cocotb-config --makefiles)/Makefile.sim
