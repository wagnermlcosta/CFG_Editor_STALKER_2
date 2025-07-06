import re

def apply_operation(current, value, operation):
    if operation == "+":
        return current + value
    elif operation == "-":
        return current - value
    elif operation == "*":
        return current * value
    elif operation == "/":
        return current / value
    return current

def process_lines(lines, config):
    key = config["key"]
    line_start = config["line_start"]
    line_end = config["line_end"]
    replace_only = config["replace_only"]
    value_num = config["value_num"]
    operation = config["operation"]

    pattern = re.compile(rf"^(\s*{re.escape(key)}\s*=\s*)(.+?)(\s*)$", re.IGNORECASE)
    modified_lines = []

    for i, line in enumerate(lines, start=1):
        if not (line_start <= i <= line_end):
            modified_lines.append(line)
            continue

        match = pattern.match(line)
        if not match:
            modified_lines.append(line)
            continue

        prefix, current_value, suffix = match.groups()

        if replace_only:
            new_value_str = str(value_num)
        else:
            try:
                current_value_num = float(current_value)
                new_value = apply_operation(current_value_num, value_num, operation)
                new_value_str = str(int(new_value)) if new_value.is_integer() else f"{new_value:.6f}".rstrip('0').rstrip('.')
            except ValueError:
                modified_lines.append(line)
                continue
        
        modified_lines.append(f"{prefix}{new_value_str}{suffix}")
    
    return modified_lines
