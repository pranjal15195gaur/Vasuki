import unittest
import vm

class TestVMInstructions(unittest.TestCase):
    def setUp(self):
        # Reset VM state by loading an empty program.
        vm.load_program([])

    def test_immediate_add(self):
        # Test: R0 = R0 + immediate 3 (initially R0=0)
        OP_ADD = 0
        OP_TRAP = 4
        # Instruction format: [opcode(4)|dest(3)|src1(3)|imm_flag(1)|imm(5)]
        add_instr = (OP_ADD << 12) | (0 << 9) | (0 << 6) | (1 << 5) | (3 & 0x1F)
        halt_instr = (OP_TRAP << 12) | 0x25
        program = [add_instr, halt_instr]
        vm.load_program(program)
        vm.run_vm()
        self.assertEqual(vm.registers[0], 3)

    def test_register_add(self):
        # Test: R2 = R0 + R1 in register mode.
        OP_ADD = 0
        OP_TRAP = 4
        # Pre-set R0=10 and R1=20.
        vm.registers[0] = 10
        vm.registers[1] = 20
        # For register mode use immediate flag = 0.
        add_instr = (OP_ADD << 12) | (2 << 9) | (0 << 6) | (0 << 5) | (1 & 0x7)
        halt_instr = (OP_TRAP << 12) | 0x25
        program = [add_instr, halt_instr]
        vm.load_program(program)
        vm.run_vm()
        self.assertEqual(vm.registers[2], 30)

    def test_ld(self):
        # Test: Load a constant from memory using LD.
        OP_LD = 1
        OP_TRAP = 4
        # We choose destination R3 and offset = 1.
        ld_instr = (OP_LD << 12) | (3 << 9) | (1 & 0x1FF)
        halt_instr = (OP_TRAP << 12) | 0x25
        # Build a program of length at least 3.
        program = [0] * 3
        program[0] = ld_instr
        # When LD executes, PC is incremented to 1;
        # It will load memory[PC + offset] = memory[1+1] = memory[2]
        constant_val = 12345
        program[2] = constant_val
        # Place a HALT at index 1.
        program[1] = halt_instr
        vm.load_program(program)
        vm.run_vm()
        self.assertEqual(vm.registers[3], constant_val)

    def test_st(self):
        # Test: Store value from a register into memory.
        OP_ST = 2
        OP_TRAP = 4
        # Set R4 to a known value.
        vm.registers[4] = 987
        # Use offset = 2 so that the store goes to memory[PC + offset].
        st_instr = (OP_ST << 12) | (4 << 9) | (2 & 0x1FF)
        halt_instr = (OP_TRAP << 12) | 0x25
        # Build a program of length at least 4.
        program = [st_instr, halt_instr] + [0]*2
        # After executing ST, with PC starting at 0:
        # PC becomes 1, then memory[1+2] i.e. memory[3] is updated.
        vm.load_program(program)
        vm.run_vm()
        self.assertEqual(vm.memory[3], 987)

    def test_jmp(self):
        # Test: Jump to a target address from a register.
        OP_JMP = 3
        OP_TRAP = 4
        # Set R5 to the jump target address (e.g. 10).
        vm.registers[5] = 10
        jmp_instr = (OP_JMP << 12) | (5 << 9)
        halt_instr = (OP_TRAP << 12) | 0x25
        # Build a program with length >= 11.
        program = [0] * 11
        program[0] = jmp_instr
        # Ensure the jump target holds a HALT instruction.
        program[10] = halt_instr
        vm.load_program(program)
        vm.run_vm()
        # After JMP, the program counter should have been set to the jump target.
        self.assertEqual(vm.PC, 10)

if __name__ == "__main__":
    unittest.main()
