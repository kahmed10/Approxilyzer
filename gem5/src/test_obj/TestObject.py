from m5.params import *
from m5.SimObject import SimObject

class TestObject(SimObject):
    type = 'TestObject'
    cxx_class = 'FaultInjector::TestObject'
    cxx_header = 'test_obj/test_object.hh'

    injReg = Param.String("", "Register to inject into")
    injBit = Param.Int(0,"Bit position to flip")
    injTick = Param.Tick(0, "tick to inject fault")
    regType = Param.Int(0, "type of register (0 = int, 1 = float)")