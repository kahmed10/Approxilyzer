#include "debug/Inj.hh"
#include "sim/sim_exit.hh"
#include "injector/injector.hh"

#include <fstream>
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

Injector::Injector(InjectorParams *params) : 
    SimObject(params),
    injBit(params->injBit),
    injTick(params->injTick),
    injReg(params->injReg),
    regType(params->regType),
    timeoutVal(params->timeout),
    goldenFile(params->goldenFile)
{
    

    if (goldenFile != "")
    {
        

        std::ifstream goldFile(goldenFile);
        if (goldFile.is_open())
        {
            std::string line, strInjTick;
            bool started = false;

            strInjTick = std::to_string(injTick); // look for first tick before filling vector

            while (std::getline(goldFile, line))
            {
                if (!started)
                {
                    if (line.find(strInjTick) != std::string::npos)
                    {
                        started = true;
                    }
                }
                if (started)
                    goldenTrace.push_back(line);
            }
            goldFile.close();
        }
    }
    

    //DPRINTF("Testing object!\n");
}

void Injector::PerformFI(ThreadContext* _thread, Tick _when, 
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

void Injector::trackState(std::string faultyTrace, std::string goldenTrace)
{
    if (goldenTrace != faultyTrace)
    {
        exitSimLoop("Diff trace\n");
    }
}

}   // end namespace


FaultInjector::Injector* InjectorParams::create()
{
    return new FaultInjector::Injector(this);
}

