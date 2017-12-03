#include "debug/TestObj.hh"
#include "test_obj/test_object.hh"

#include <iostream>

using namespace X86ISA;

namespace FaultInjector
{

void FI::FlipBit(Tick _injTick, IntRegIndex injR, int injBit) // add bit position as parameter
{
    uint64_t currVal = thread->readIntReg(injR);
    uint64_t bitMask = 1 << injBit;
    
    thread->setIntReg(injR, currVal ^ bitMask); // flip bit using mask
}

void FI::FlipBit(Tick _injTick, FloatRegIndex injR, int injBit) // add bit position as parameter
{
    uint64_t currVal = thread->readFloatReg(injR);
    uint64_t bitMask = 1 << injBit;
    
    thread->setIntReg(injR, currVal ^ bitMask); // flip bit using mask
}

TestObject::TestObject(TestObjectParams *params) : 
    SimObject(params),
    injBit(params->injBit),
    injTick(params->injTick),
    injReg(params->injReg),
    regType(params->regType)
{
    DPRINTF(TestObj, "Testing object!\n");
}

void TestObject::PerformFI(ThreadContext* _thread, Tick _when, 
                      Tick _injTick, std::string desiredR, int injBit, int regType)
{
    FI fi(_thread, _when);
    if (regType == 0)   // int register
    {   
        IntRegIndex injR = intRegConverter[desiredR];
        fi.FlipBit(_injTick, injR, injBit);
    }
    else if (regType == 1) // float register
    {
        FloatRegIndex injR = floatRegConverter[desiredR];
        fi.FlipBit(_injTick, injR, injBit);
    }
}

}   // end namespace


FaultInjector::TestObject* TestObjectParams::create()
{
    return new FaultInjector::TestObject(this);
}

