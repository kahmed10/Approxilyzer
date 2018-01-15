#ifndef __TEST_OBJ_TEST_OBJECT_HH__
#define __TEST_OBJ_TEST_OBJECT_HH__

#include "params/Injector.hh"
#include "sim/sim_object.hh"

#include "arch/x86/regs/int.hh"
#include "arch/x86/regs/float.hh"
#include "base/bigint.hh"
#include "base/types.hh"
#include "cpu/inst_seq.hh"
#include "cpu/static_inst.hh"

class ThreadContext;


using namespace X86ISA;

namespace FaultInjector {



// convert string to correct register index
static std::map<std::string, IntRegIndex> intRegConverter =
{
    {"rax", IntRegIndex::INTREG_RAX},
    {"eax", IntRegIndex::INTREG_EAX},
    {"ax", IntRegIndex::INTREG_AX},
    {"al", IntRegIndex::INTREG_AL},

    {"rcx", IntRegIndex::INTREG_RCX},
    {"ecx", IntRegIndex::INTREG_ECX},
    {"cx", IntRegIndex::INTREG_CX},
    {"cl", IntRegIndex::INTREG_CL},

    {"rdx", IntRegIndex::INTREG_RDX},
    {"edx", IntRegIndex::INTREG_EDX},
    {"dx", IntRegIndex::INTREG_DX},
    {"dl", IntRegIndex::INTREG_DL},

    {"rbx", IntRegIndex::INTREG_RBX},
    {"ebx", IntRegIndex::INTREG_EBX},
    {"bx", IntRegIndex::INTREG_BX},
    {"bl", IntRegIndex::INTREG_BL},

    {"rsp", IntRegIndex::INTREG_RSP},
    {"esp", IntRegIndex::INTREG_ESP},
    {"sp", IntRegIndex::INTREG_SP},
    {"spl", IntRegIndex::INTREG_SPL},
    {"ah", IntRegIndex::INTREG_AH},

    {"rbp", IntRegIndex::INTREG_RBP},
    {"ebp", IntRegIndex::INTREG_EBP},
    {"bp", IntRegIndex::INTREG_BP},
    {"bpl", IntRegIndex::INTREG_BPL},
    {"ch", IntRegIndex::INTREG_CH},

    {"rsi", IntRegIndex::INTREG_RSI},
    {"esi", IntRegIndex::INTREG_ESI},
    {"si", IntRegIndex::INTREG_SI},
    {"sil", IntRegIndex::INTREG_SIL},
    {"dh", IntRegIndex::INTREG_DH},

    {"rdi", IntRegIndex::INTREG_RDI},
    {"edi", IntRegIndex::INTREG_EDI},
    {"di", IntRegIndex::INTREG_DI},
    {"dil", IntRegIndex::INTREG_DIL},
    {"bh", IntRegIndex::INTREG_BH},

    {"r8", IntRegIndex::INTREG_R8},
    {"r9", IntRegIndex::INTREG_R9},
    {"r10", IntRegIndex::INTREG_R10},
    {"r11", IntRegIndex::INTREG_R11},
    {"r12", IntRegIndex::INTREG_R12},
    {"r13", IntRegIndex::INTREG_R13},
    {"r14", IntRegIndex::INTREG_R14},
    {"r15", IntRegIndex::INTREG_R15}
};

// each FP register may need different bit flips depending on which
// data we are accessing. An example is "movapd %xmm1,%xmm2" 
// that moves xmm1_high->xmm2_high, and xmm1_low->xmm2_low
static std::map<std::string, FloatRegIndex> floatRegConverter =
{
    {"xmm0", FloatRegIndex::FLOATREG_XMM0_LOW},
    {"xmm0_low", FloatRegIndex::FLOATREG_XMM0_LOW},
    {"xmm0_high", FloatRegIndex::FLOATREG_XMM0_HIGH},

    {"xmm1", FloatRegIndex::FLOATREG_XMM1_LOW},
    {"xmm1_low", FloatRegIndex::FLOATREG_XMM1_LOW},
    {"xmm1_high", FloatRegIndex::FLOATREG_XMM1_HIGH},

    {"xmm2", FloatRegIndex::FLOATREG_XMM2_LOW},
    {"xmm2_low", FloatRegIndex::FLOATREG_XMM2_LOW},
    {"xmm2_high", FloatRegIndex::FLOATREG_XMM2_HIGH},

    {"xmm3", FloatRegIndex::FLOATREG_XMM3_LOW},
    {"xmm3_low", FloatRegIndex::FLOATREG_XMM3_LOW},
    {"xmm3_high", FloatRegIndex::FLOATREG_XMM3_HIGH},

    {"xmm4", FloatRegIndex::FLOATREG_XMM4_LOW},
    {"xmm4_low", FloatRegIndex::FLOATREG_XMM4_LOW},
    {"xmm4_high", FloatRegIndex::FLOATREG_XMM4_HIGH},

    {"xmm5", FloatRegIndex::FLOATREG_XMM5_LOW},
    {"xmm5_low", FloatRegIndex::FLOATREG_XMM5_LOW},
    {"xmm5_high", FloatRegIndex::FLOATREG_XMM5_HIGH},

    {"xmm6", FloatRegIndex::FLOATREG_XMM6_LOW},
    {"xmm6_low", FloatRegIndex::FLOATREG_XMM6_LOW},
    {"xmm6_high", FloatRegIndex::FLOATREG_XMM6_HIGH},

    {"xmm7", FloatRegIndex::FLOATREG_XMM7_LOW},
    {"xmm7_low", FloatRegIndex::FLOATREG_XMM7_LOW},
    {"xmm7_high", FloatRegIndex::FLOATREG_XMM7_HIGH},

    {"xmm8", FloatRegIndex::FLOATREG_XMM8_LOW},
    {"xmm8_low", FloatRegIndex::FLOATREG_XMM8_LOW},
    {"xmm8_high", FloatRegIndex::FLOATREG_XMM8_HIGH},

    {"xmm9", FloatRegIndex::FLOATREG_XMM9_LOW},
    {"xmm9_low", FloatRegIndex::FLOATREG_XMM9_LOW},
    {"xmm9_high", FloatRegIndex::FLOATREG_XMM9_HIGH},

    {"xmm10", FloatRegIndex::FLOATREG_XMM10_LOW},
    {"xmm10_low", FloatRegIndex::FLOATREG_XMM10_LOW},
    {"xmm10_high", FloatRegIndex::FLOATREG_XMM10_HIGH},

    {"xmm11", FloatRegIndex::FLOATREG_XMM11_LOW},
    {"xmm11_low", FloatRegIndex::FLOATREG_XMM11_LOW},
    {"xmm11_high", FloatRegIndex::FLOATREG_XMM11_HIGH},
    
    {"xmm12", FloatRegIndex::FLOATREG_XMM12_LOW},
    {"xmm12_low", FloatRegIndex::FLOATREG_XMM12_LOW},
    {"xmm12_high", FloatRegIndex::FLOATREG_XMM12_HIGH},

    {"xmm13", FloatRegIndex::FLOATREG_XMM13_LOW},
    {"xmm13_low", FloatRegIndex::FLOATREG_XMM13_LOW},
    {"xmm13_high", FloatRegIndex::FLOATREG_XMM13_HIGH},

    {"xmm14", FloatRegIndex::FLOATREG_XMM14_LOW},
    {"xmm14_low", FloatRegIndex::FLOATREG_XMM14_LOW},
    {"xmm14_high", FloatRegIndex::FLOATREG_XMM14_HIGH},

    {"xmm15", FloatRegIndex::FLOATREG_XMM15_LOW},
    {"xmm15_low", FloatRegIndex::FLOATREG_XMM15_LOW},
    {"xmm15_high", FloatRegIndex::FLOATREG_XMM15_HIGH}
};
// TODO: add PC (thread->instAddr())
class FI
{
  protected:
    Tick when;
    ThreadContext* thread;
  public:
    FI(ThreadContext* _thread, Tick _when)
        : when(_when), thread(_thread)
    { }
    void FlipBit(Tick _injTick, IntRegIndex injR, int injBit);
    void FlipBit(Tick _injTick, FloatRegIndex injR, int injBit);
};

class Injector : public SimObject
{    
  public:
    int injBit;
    Tick injTick;
    std::string injReg;
    int regType;
    Tick timeoutVal; // = 10000000000; // test timeout
    std::string goldenFile;

    std::vector<std::string> goldenTrace;

    Injector(InjectorParams *p);
    void PerformFI(ThreadContext* _thread, Tick _when,
                   Tick _injTick, std::string desiredR, int injBit, int regType);
    void trackState(std::string faultyTrace, std::string goldenTrace);
};

}   // end namespace




#endif
