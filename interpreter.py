import platform, sys
from os import system as cmd

def clear(): # Cross-platform console clearer
  ostype = platform.system()
  if ostype == "Linux" or ostype == "Darwin":
    cmd("clear")
  else:
    cmd("cls")

def interpret(code):
    code_ptr = 0
    data_ptr = 0
    data = [0] * 100000
    output = []

    while code_ptr < len(code):
        instruction = code[code_ptr]
        pointer_increment = 0

        # NORMAL BF INSTRUCTIONS
        if instruction == ">":
            data_ptr += 1
        elif instruction == "<":
            data_ptr -= 1
        elif instruction == "+":
            data[data_ptr] = (data[data_ptr] + 1)
        elif instruction == "-":
            data[data_ptr] = (data[data_ptr] - 1)
        elif instruction == ".":
            output.append(chr(data[data_ptr]))
        elif instruction == ",":
            data[data_ptr] = ord(input()[0])
        elif instruction == "[" and data[data_ptr] == 0:
            loop_depth = 1
            while loop_depth > 0:
                code_ptr += 1
                if code[code_ptr] == "[":
                    loop_depth += 1
                elif code[code_ptr] == "]":
                    loop_depth -= 1
        elif instruction == "]" and data[data_ptr] != 0:
            loop_depth = 1
            while loop_depth > 0:
                code_ptr -= 1
                if code[code_ptr] == "]":
                    loop_depth += 1
                elif code[code_ptr] == "[":
                    loop_depth -= 1
        
        # BF++ !!
        elif instruction == "!":
            output.append(str(data[data_ptr]))
        elif instruction == "=":
            value1 = data[data_ptr-2]
            value2 = data[data_ptr-1]
            if value1 == value2:
                data[data_ptr] = 1
            else:
                data[data_ptr] = 0

        code_ptr = code_ptr + 1 + pointer_increment

    return ''.join(output)

# Check if the filename argument is provided
if len(sys.argv) < 2:
    print("Usage: python interpreter.py <filename>")
    sys.exit(1)

# Read the Brainfuck code from the file
filename = sys.argv[1]
try:
    with open(filename, "r") as file:
        brainfuck_code = file.read()
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)

# Interpret the Brainfuck code
output = interpret(brainfuck_code)
print(output)