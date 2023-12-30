# Modi-sic-one-pass-assembler
The Modi-SIC One-Pass Assembler Project (Type 2) is designed to create a program that performs one-pass assembly for the Modified Simple Instruction Computer (modi-SIC). The assembler will translate assembly code into machine code compatible with the Modified Simplified Instructional Computer.

The modi-SIC architecture retains the instruction set and Format 3 instructions from the original SIC (Simple
Instruction Computer). It also includes the concept of reserving variables in memory using directives such as
BYTE, WORD, RESB, and RESW.

Key Modifications and Extensions:
• Format 1 Instructions: Modi-SIC extends its capabilities by introducing Format 1 instructions,
expanding the range of supported operations.
• Immediate Instructions (Format 3): Modi-SIC introduces immediate instructions, allowing for the
handling of immediate values passed as integers. This provides greater flexibility in executing
instructions.
• Relocation: The Modi-SIC also supports relocation by using the masking bits in the text records, where
1 denotes memory location that needs modification and 0 otherwise
Instructions Handling:
The assembler will process the assembly code in a single pass, generating machine code (HTE records) for
execution on the modi-SIC. It will consider both the original SIC Format 3 instructions and the newly
introduced Format 1 instructions and immediate instructions.
Project Scope:
This project aims to streamline the assembly process for modi-SIC, providing an efficient tool for converting
assembly code into executable machine code in a single pass. The one-pass assembler will read the
assembly code, allocate memory, and generate the corresponding relocatable machine code for
execution on modi-SIC. It will handle symbol resolution, directive processing, and object code generation
(HTE) in a single pass.
