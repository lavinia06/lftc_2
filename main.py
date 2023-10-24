import re

# Define regular expressions for different token types
keyword_pattern = re.compile(r'def|int|if|else|write_console')
identifier_pattern = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
constant_pattern = re.compile(r'\d+(\.\d+)?')
operator_pattern = re.compile(r'==|>|\.')
delimiter_pattern = re.compile(r'[()\[\].]')
string_literal_pattern = re.compile(r'"[^"]*"')

# Initialize symbol table and FIP table
symbol_table = {}
fip_table = []

current_position = 1

def add_token_to_symbol_table(token):
    global current_position
    if token not in symbol_table:
        symbol_table[token] = current_position
        current_position += 1

def add_token_to_fip(code):
    global current_position
    if code == 0 or code == 2:
        fip_table.append((code, current_position))
    else:
        fip_table.append((code, ""))


def lexical_analysis(source_code):
    i = 0

    while i < len(source_code):
        char = source_code[i]

        if char.isalpha() or char == '_':
            token = ""
            while i < len(source_code) and (char.isalnum() or char == '_'):
                token += char
                i += 1
                if i < len(source_code):
                    char = source_code[i]

            if keyword_pattern.match(token):
                add_token_to_fip(3)  # Use code 3 for keywords
            else:
                if len(token) > 13:
                    print_red(f"Eroare: Identificatorul are lungimea > 13 '{token}' la poziția {i}.")
                    return
                else:
                    add_token_to_symbol_table(token)
                    add_token_to_fip(0)  # Use code 0 for identifiers

        elif char.isdigit() or char == '-':
            token = ""
            while i < len(source_code) and (char.isdigit() or char == '-'):
                token += char
                i += 1
                if i < len(source_code):
                    char = source_code[i]

            if constant_pattern.match(token):
                add_token_to_symbol_table(token)
                add_token_to_fip(2)  # Use code 2 for constants
            else:
                print_red(f"Eroare: Constantă nevalidă '{token}' la poziția {i}.")
                return

        elif char in "+-*/=><(){}.":
            token = char
            i += 1
            add_token_to_fip(4)

        elif char in '[]':
            token = char
            i += 1
            add_token_to_fip(4)  # You may want to define a different code for '[' and ']' in your language

        elif char == ';':
            print_red(f"Eroare: Caracterul ';' nu este permis la poziția {i}.")
            return

        elif char == "\n" or char.isspace():
            i += 1

        elif char == '"':
            match = string_literal_pattern.match(source_code[i:])
            if match:
                token = match.group(0)
                add_token_to_fip(5)
                i += len(token)

        else:
            print_red(f"Eroare: Caracter necunoscut '{char}' la poziția {i}.")
            return

    return fip_table

def print_fip(output_file):
    with open(output_file, 'w') as file:
        file.write("Cod atom | Pozitie in TS\n")
        for code, atom in fip_table:
            file.write(f"{code}   | {atom}\n")

def order_symbol_table_lexicographically():
    sorted_symbol_table = dict(sorted(symbol_table.items()))
    return sorted_symbol_table

def write_symbol_table(output_file):
    sorted_symbol_table = order_symbol_table_lexicographically()
    with open(output_file, 'w') as file:
        file.write("Pozitie | Atom lexical\n")
        for position, token in sorted_symbol_table.items():
            file.write(f"{token}        | {position}\n")

def read_source_code(input_file):
    with open(input_file, 'r') as file:
        source_code = file.read()
    return source_code

def print_red(text):
    red = "\033[91m"
    reset = "\033[0m"
    print(f"{red}{text}{reset}")

input_file = "input.txt"
output_symbol_table_file = "output_symbol_table.txt"
output_fip_file = "output_fip.txt"

source_code = read_source_code(input_file)

lexical_analysis(source_code)
write_symbol_table(output_symbol_table_file)
print_fip(output_fip_file)
print(f"Tabelele au fost scrise în fișierele {output_symbol_table_file} și {output_fip_file}")
