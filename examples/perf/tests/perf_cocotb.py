import cocotb
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure
import random
from IPython import embed
import numpy as np
from pytictoc import TicToc


class settings(object):
    def __init__(self):
        self.npoints = 500
        self.dinArate = 1000
        self.dinBrate = 1500
        self.period = 2

async def genstrobe(sig, clkobj, clk, N):
    waiting = Timer((clkobj.period * N) - 2)
    while True:
        sig <= 0
        await waiting
        await RisingEdge(clk)
        sig <= 1
        await RisingEdge(clk)

async def reset(dut):
    dut.resetb <= 0
    await Timer(5, 'us')
    dut.resetb <= 1
    await Timer(5, 'us')

@cocotb.test()
async def forking(dut):
    """perf forking test"""

    t = TicToc()
    tb = settings()

    await reset(dut)

    clkobj = Clock(dut.clk, tb.period, 'us')
    cocotb.fork(clkobj.start())

    t.tic()
    cocotb.fork(genstrobe(dut.dinA, clkobj, dut.clk, tb.dinArate))
    cocotb.fork(genstrobe(dut.dinB, clkobj, dut.clk, tb.dinBrate))
    dinstrobe = RisingEdge(dut.dinA)

    for cycle in range(tb.npoints):
        await dinstrobe
        if(cycle%100 == 0):
            dut._log.info("Sim progress...{} %".format(int(100*float(cycle)/tb.npoints)))  
    t.toc()
    print(t.elapsed)   


@cocotb.test()
async def oneloop(dut):
    """perf oneloop test"""

    t = TicToc()
    tb = settings()

    await reset(dut)

    clkobj = Clock(dut.clk, tb.period, 'us')
    cocotb.fork(clkobj.start())

    t.tic()
    k = 0
    for cycle in range(tb.dinArate*tb.npoints): 
        await (RisingEdge(dut.clk))  
        if (cycle%tb.dinArate)==0:
            k = k+1
            dut.dinA <= 1
            if(k%100 == 0):
                dut._log.info("Sim progress...{} %".format(int(100*float(k)/tb.npoints)))                    
        else:
            dut.dinA <= 0

        if (cycle%tb.dinBrate)==0:
            dut.dinB <= 1       
        else:
            dut.dinB <= 0    

    t.toc()
    print(t.elapsed)   

