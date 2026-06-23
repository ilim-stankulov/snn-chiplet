# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
SRC_DIR = $(PWD)/../src

ifneq ($(SYSTEM),yes)

SIM_BUILD           = sim_build/rtl
VERILOG_SOURCES    += $(SRC_DIR)/project.v
VERILOG_SOURCES    += $(SRC_DIR)/lif_components.v
VERILOG_SOURCES    += $(PWD)/tb.v
TOPLEVEL            = tb
COCOTB_TEST_MODULES = test

else

SIM_BUILD           = sim_build/system
VERILOG_SOURCES    += $(SRC_DIR)/lif_components.v
VERILOG_SOURCES    += $(SRC_DIR)/snn_tile.v
VERILOG_SOURCES    += $(SRC_DIR)/d2d_link.v
VERILOG_SOURCES    += $(SRC_DIR)/system_top.v
VERILOG_SOURCES    += $(PWD)/tb_system.v
TOPLEVEL            = tb_system
COCOTB_TEST_MODULES = test_system

endif

COMPILE_ARGS += -I$(SRC_DIR)

include $(shell cocotb-config --makefiles)/Makefile.sim
