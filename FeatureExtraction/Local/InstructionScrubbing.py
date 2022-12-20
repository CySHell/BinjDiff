from binaryninja import *
from datasketch import MinHash, MinHashLSH

PRINT_DBG_ALL = 0
PRINT_DBG_UNKNOWN_ONLY = 0
SCRUB_SEPERATOR = "-"


def printdbg(s, unknown=False):
    if (unknown and PRINT_DBG_UNKNOWN_ONLY) or PRINT_DBG_ALL:
        print(s)


def IsHighLevelIlInstruction(obj) -> bool:
    return isinstance(obj, HighLevelILInstruction)


def IsVariable(obj) -> bool:
    return isinstance(obj, Variable)


def ParseOperands(instr: HighLevelILInstruction) -> str:
    current_scrubbed_instruction = ""
    for operand in instr.operands:
        if IsHighLevelIlInstruction(operand):
            current_scrubbed_instruction += ScrubHlilInstruction(operand)
        elif IsVariable(operand):
            current_scrubbed_instruction += ScrubVariable(operand)
        else:
            printdbg(f"ParseOperands: Unknown operand {operand}, type {type(operand)}")
    return current_scrubbed_instruction


def DefaultScrubber(instr: HighLevelILInstruction) -> str:
    printdbg(f"DefaultScrubber: Scrubbing {instr}")
    scrubbed_instruction: str = ""
    scrubbed_instruction += instr.operation.name + SCRUB_SEPERATOR
    scrubbed_instruction += ParseOperands(instr)
    return scrubbed_instruction


def ScrubVariable(var: Variable) -> str:
    printdbg(f"ScrubVariable: Scrubbing {var}")
    scrubbed_instr = ""
    scrubbed_instr += SCRUB_SEPERATOR + var.type.type_class.name
    scrubbed_instr += SCRUB_SEPERATOR + var.source_type.name
    return scrubbed_instr


# HighLevelILOperation.HLIL_CONST_PTR
def ScrubHlilConstPtr(instr: HighLevelILInstruction) -> str:
    printdbg(f"ScrubHlilConstPtr: Scrubbing {instr}")
    return instr.operation.name


# HighLevelILOperation.HLIL_VAR_DECLARE
def ScrubHlilVarDeclare(instr: HighLevelILInstruction) -> str:
    scrubbed_instr: str = instr.operation.name
    printdbg(f"ScrubHlilVarDeclare: Scrubbing {instr}")
    for var in instr.vars:
        if IsHighLevelIlInstruction(var):
            var: HighLevelILInstruction
            scrubbed_instr += ScrubHlilInstruction(var)
        else:
            var: Variable
            scrubbed_instr += ScrubVariable(var)
    return scrubbed_instr


# HighLevelILOperation.HLIL_DEREF
def ScrubHlilDeref(instr: HighLevelILInstruction) -> str:
    return DefaultScrubber(instr)


# HighLevelILOperation.HLIL_VAR_INIT
def ScrubHlilVarInit(instr: HighLevelILInstruction) -> str:
    instr: HighLevelILVarInit
    printdbg(f"ScrubHlilVarInit: Scrubbing {instr}")
    scrubbed_instr: str = instr.operation.name
    scrubbed_instr += SCRUB_SEPERATOR + f"SRC{ScrubHlilInstruction(instr.src)}"
    scrubbed_instr += SCRUB_SEPERATOR + f"DEST{ScrubVariable(instr.dest)}"
    return scrubbed_instr


# HighLevelILOperation.HLIL_IF
def ScrubHlilIf(instr: HighLevelILInstruction) -> str:
    return DefaultScrubber(instr)


# HighLevelILOperation.HLIL_CONST
def ScrubHlilConst(instr: HighLevelILInstruction) -> str:
    instr: HighLevelILConst
    printdbg(f"ScrubHlilConst: Scrubbing {instr}")
    scrubbed_instr: str = instr.operation.name
    scrubbed_instr += SCRUB_SEPERATOR + instr.value.type.name
    scrubbed_instr += SCRUB_SEPERATOR + str(instr.value.value)
    return scrubbed_instr


# HighLevelILOperation.HLIL_RET
def ScrubHlilRet(instr: HighLevelILInstruction) -> str:
    return DefaultScrubber(instr)


# HighLevelILOperation.HLIL_VAR
def ScrubHlilVar(instr: HighLevelILInstruction) -> str:
    return DefaultScrubber(instr)


def ScrubHlilInstruction(instr: HighLevelILInstruction) -> str:
    current_scrubbed_instruction: str = ""
    current_scrubbed_instruction += instr.operation.name
    printdbg(f"ScrubHlilInstruction: Scrubbing instruction {hex(instr.address)}")
    for operand in instr.operands:
        printdbg(f"ScrubHlilInstruction: Scrubbing operand {operand} - {type(operand)}")
        if IsHighLevelIlInstruction(operand):
            if operand.operation is HighLevelILOperation.HLIL_CONST_PTR:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilConstPtr(operand)
            elif operand.operation is HighLevelILOperation.HLIL_VAR_DECLARE:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilVarDeclare(operand)
            elif operand.operation is HighLevelILOperation.HLIL_VAR_INIT:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilVarInit(operand)
            elif operand.operation is HighLevelILOperation.HLIL_DEREF:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilDeref(operand)
            elif operand.operation is HighLevelILOperation.HLIL_IF:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilIf(operand)
            elif operand.operation is HighLevelILOperation.HLIL_CONST:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilConst(operand)
            elif operand.operation is HighLevelILOperation.HLIL_RET:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilRet(operand)
            elif operand.operation is HighLevelILOperation.HLIL_VAR:
                current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubHlilVar(operand)
            else:
                if csi := DefaultScrubber(operand):
                    current_scrubbed_instruction += SCRUB_SEPERATOR + csi
                else:
                    printdbg(f"ScrubHlilInstruction: Unknown operand - {operand}, addr: {hex(operand.address)}", True)
        elif IsVariable(operand):
            current_scrubbed_instruction += SCRUB_SEPERATOR + ScrubVariable(operand)
        else:
            printdbg(f"ScrubHlilInstruction: Unknown operand - {operand}, instruction address: {hex(instr.address)}",
                     False)
    return current_scrubbed_instruction


global_lsh = MinHashLSH(
    threshold=0.5, num_perm=128, storage_config={
        'type': 'redis',
        'redis': {'host': '192.168.10.130', 'port': 6379},
    }
)
func_count = 0
for f in bv.functions:
    if f.name.startswith("_sub"):
        continue
    instr_lsh = MinHash(num_perm=128)
    try:
        # print(f"Processing function: {func_count}\{len(bv.functions)}")
        func_count += 1
        if len(list(f.instructions)) > 4:
            for i in f.hlil.instructions:
                instr_lsh.update(ScrubHlilInstruction(i).encode("utf8"))
    except Exception as e:
        print(f"Exception processing function {f}\nException: {e}")
    # """
    result = global_lsh.query(instr_lsh)
    if result:
        print(f"Processing function: {hex(f.start)}")
        print(result)
    # """
    # global_lsh.insert(f"{f.name}_{hex(f.start - bv.start)}", instr_lsh)
