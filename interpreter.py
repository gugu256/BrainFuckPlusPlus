import platform, sys
from os import system as cmd

def clear(): # Cross-platform console clearer
  ostype = platform.system()
  if ostype == "Linux" or ostype == "Darwin":
    cmd("clear")
  else:
    cmd("cls")

characters = []

characters += " " + "\n" + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789><+-.()[,]$=!{;}~?|*'&@_/§:" + '\\'

def interpret(code):
    code_ptr = 0
    can_increment = True
    data_ptr = 0
    secondary_digit = 0
    data = [0] * 50000
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
            output.append(characters[data[data_ptr]])
        elif instruction == ",":
            data[data_ptr] = int(input()[0])
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
        elif instruction == "$": # Output the NUMBER of the pointer 
            output.append(str(data[data_ptr]))

        elif instruction == "=": # == equivalent # 1, 1, 0 --> 1, 1, 1 | 1, 0, 1, --> 1, 0, 0
            value1 = data[data_ptr-2]
            value2 = data[data_ptr-1]
            if value1 == value2:
                data[data_ptr] = 1
            else:
                data[data_ptr] = 0

        elif instruction == "!": # != equivalent # 1, 2, 0 --> 1, 2, 1
            value1 = data[data_ptr-2]
            value2 = data[data_ptr-1]
            if value1 != value2:
                data[data_ptr] = 1
            else:
                data[data_ptr] = 0

        elif instruction == "{": # < equivalent # 1, 2, 0 -- > 1, 2, 1
            value1 = data[data_ptr-2]
            value2 = data[data_ptr-1]
            if value1 < value2:
                data[data_ptr] = 1
            else:
                data[data_ptr] = 0

        elif instruction == "}": # > equivalent # 2, 1, 0 --> 2, 1, 1
            value1 = data[data_ptr-2]
            value2 = data[data_ptr-1]
            if value1 > value2:
                data[data_ptr] = 1
            else:
                data[data_ptr] = 0

        elif instruction == "~": # Swap The Values # 1, 2 --> 2, 1
            stock = data[data_ptr]
            data[data_ptr] = data[data_ptr-1]
            data[data_ptr-1] = stock
        
        elif instruction == "?":
            output.append(str(data_ptr))
        
        elif instruction == ";": # "Comment" (ignore next instruction)
            pointer_increment += 1
        
        elif instruction == "|": # Copy value to the next bit(?) # 1, 0 --> 1, 1
            data[data_ptr] = data[data_ptr-1]

        elif instruction == "*": # print THE WHOLE array
            for bit in data:
                print(str(bit), end=", ")
        
        elif instruction == "'": # Add the last two bits # 1, 3, 0 --> 1, 3, 4
            data[data_ptr] = data[data_ptr-1] + data[data_ptr-2]
        
        elif instruction == "_": # Substract the last two bits # 1, 3, 0 --> 1, 3, -2
            data[data_ptr] =  data[data_ptr-2] - data[data_ptr-1]
        
        elif instruction == "&": # Multiply the last two bits # 2, 2, 0 --> 2, 2, 4
            data[data_ptr] =  data[data_ptr-1] * data[data_ptr-2]

        elif instruction == "/": # Divide the last two digits # 5, 2, 0 --> 5, 2, 2.5
            data[data_ptr] = round(data[data_ptr-2] / data[data_ptr-1], 1)
        
        elif instruction == "@": # Add 0.1 to the bit
            data[data_ptr] += 0.1

        elif instruction == "§": # Substract 0.1 to the bit
            data[data_ptr] -= 0.1
        
        elif instruction == "(":
            data[data_ptr] = secondary_digit

        elif instruction == ")":
            secondary_digit = data[data_ptr]

        # TO DO :
        # ()%"
        if can_increment:
            code_ptr = code_ptr + 1 + pointer_increment
        else:
            pass

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