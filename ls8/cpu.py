"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.SP = 7

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
    


        # For now, we've just hardcoded a program:


        # HALT = 0b00000001
        # PRN = 0b01000111
        # LDI = 0b10000010
        # MUL = 10100010

        # program = [
        #     # From print8.ls8
        #     LDI, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     LDI, # LDI R1,9
        #     0b00000001,
        #     0b00001001,
        #     MUL, # MUL R0,R1
        #     0b00000000,
        #     0b00000001,
        #     PRN, # PRN R0
        #     0b00000000,
        #     HALT # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                #print(v)
                self.ram[address] = v
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False
        HALT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        # SP = 7

        while not halted:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[operand_a]) 
                self.pc += 2

            elif instruction == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                self.pc += 3


            elif instruction == PUSH:
                # Decrement the SP
                self.SP -= 1
                # Get register number
                # Get value out of the register
                val = self.reg[operand_a]         
                # Store value in memory at SP
                # top_of_stack = self.reg[self.SP]
                self.ram[self.SP] = val
                self.pc += 2

            elif instruction == POP:
                # Get register number
                # Get value out of the register
                val = self.ram[self.SP]    
                # Store value in memory at SP  
                self.reg[operand_a] = val
                # Increment the SP
                self.SP += 1
                self.pc += 2

            elif instruction == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3

            elif instruction == CALL:
                return_addr = self.pc + 2
                # Push it on the stack
                self.SP -= 1
                top_of_stack_addr = self.reg[self.SP]
                self.ram[top_of_stack_addr] = return_addr
                # Set the PC to the subroutine addr
                # reg_num = memory[pc + 1]
                subroutine_addr = self.reg[operand_a]
                self.pc = subroutine_addr

            elif instruction == RET:
                # Pop the return addr off stack
                top_of_stack_addr = self.reg[self.SP]
                return_addr = self.ram[top_of_stack_addr]
                self.reg[self.SP] += 1
                # Store it in the PC
                self.pc = return_addr


            
            elif instruction == HALT:
                halted = True

            else:
                print(f'unknown instruction {instruction} at address {self.pc}')

                sys.exit()
		    

                


    