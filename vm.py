import sys

MEMORY_SIZE = 1 << 16  # 65536 words
REGISTER_COUNT = 8

# Memory and registers
memory = [0] * MEMORY_SIZE
registers = [0] * REGISTER_COUNT
PC = 0         # Program Counter
COND = 1 << 1  # Initial condition flag (FL_ZRO)

# Condition flags.
FL_POS = 1 << 0
FL_ZRO = 1 << 1
FL_NEG = 1 << 2

# Opcodes.
OP_ADD  = 0  # add
OP_LD   = 1  # load
OP_ST   = 2  # store
OP_JMP  = 3  # jump
OP_TRAP = 4  # trap

# Define custom halt exception.
class VMHalt(Exception):
    pass

def sign_extend(x: int, bit_count: int) -> int:
    if x & (1 << (bit_count - 1)):
        x |= (~0 << bit_count)
    return x

def update_flags(reg: int):
    global COND
    if registers[reg] == 0:
        COND = FL_ZRO
    elif registers[reg] < 0:
        COND = FL_NEG
    else:
        COND = FL_POS

def trap_halt():
    print("HALT encountered. Stopping VM.")
    raise VMHalt()

def run_vm():
    global PC
    running = True
    try:
        while running and PC < MEMORY_SIZE:
            instr = memory[PC]
            PC += 1
            opcode = instr >> 12  # upper 4 bits as opcode

            if opcode == OP_ADD:
                # bits 11:9 destination, bits 8:6 src1, bit 5 immediate flag.
                dest = (instr >> 9) & 0x7
                src1 = (instr >> 6) & 0x7
                if (instr >> 5) & 0x1:  # immediate mode
                    imm = sign_extend(instr & 0x1F, 5)
                    registers[dest] = registers[src1] + imm
                else:
                    src2 = instr & 0x7
                    registers[dest] = registers[src1] + registers[src2]
                update_flags(dest)

            elif opcode == OP_LD:
                # bits 11:9 destination, bits 8:0 offset.
                dest = (instr >> 9) & 0x7
                offset = sign_extend(instr & 0x1FF, 9)
                registers[dest] = memory[PC + offset]
                update_flags(dest)

            elif opcode == OP_ST:
                # bits 11:9 source, bits 8:0 offset.
                src = (instr >> 9) & 0x7
                offset = sign_extend(instr & 0x1FF, 9)
                memory[PC + offset] = registers[src]

            elif opcode == OP_JMP:
                # bits 11:9 base register.
                base = (instr >> 9) & 0x7
                PC = registers[base]
                continue  # Prevent extra PC increment

            elif opcode == OP_TRAP:
                # bits 7:0 trap vector.
                trap_vector = instr & 0xFF
                if trap_vector == 0x25:  # HALT trap.
                    PC -= 1  # Roll back PC so that halt appears at proper address.
                    trap_halt()
                else:
                    print(f"Unknown trap code: 0x{trap_vector:X}")
                    running = False

            else:
                print(f"Unknown opcode: 0x{opcode:X} at PC: {PC-1}")
                running = False
    except VMHalt:
        # Halt the VM gracefully.
        running = False

def load_program(program):
    global PC, memory
    # Clear memory and reset PC.
    for i in range(MEMORY_SIZE):
        memory[i] = 0
    PC = 0
    for i, instr in enumerate(program):
        memory[i] = instr

def load_test_program():
    global PC
    for i in range(MEMORY_SIZE):
        memory[i] = 0
    PC = 0
    registers[1] = 10
    add_instr = (OP_ADD << 12) | (0 << 9) | (1 << 6) | (1 << 5) | (5 & 0x1F)
    memory[0] = add_instr
    halt_instr = (OP_TRAP << 12) | 0x25
    memory[1] = halt_instr

if __name__ == "__main__":
    try:
        load_test_program()
        run_vm()
    except VMHalt:
        pass
    for i in range(REGISTER_COUNT):
        print(f"R{i} = {registers[i]}")
