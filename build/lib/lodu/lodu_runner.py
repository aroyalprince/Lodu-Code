import sys
import os
import re
import random
import time

# --- LODU CODE CUSTOM GLOBALS ---
def custom_raand(*args):
    if len(args) == 1:
        return [random.randint(1, 100) for _ in range(args[0])]
    elif len(args) == 2:
        return random.randint(args[0], args[1])
    return random.randint(1, 100)

def lodu_interpreter(source_code):
    lines = source_code.strip().split('\n')
    variables = {}
    
    jumps = {}
    stack = []
    functions = {} 
    call_stack = [] 

    desi_globals = {
        'raand': custom_raand,
        'sabar_kar': time.sleep,
        'Array': list,
        'boolean': bool,
        'int': int,
        'str': str,
        'float': float,
        'true': True,
        'false': False,
        'naap': len 
    }

    # --- SANSKAR CHECK (Strict + Case Insensitive + Naye Errors) ---
    has_namaste = False
    has_khatm = False
    has_main = False

    for line in lines:
        # .lower() lagane se case sensitivity khatam ho jati hai
        stripped_line_lower = line.split("@@")[0].strip().lower()
        
        if "namaste" in stripped_line_lower:
            has_namaste = True
        if "khatm, tata, goodbye" in stripped_line_lower:
            has_khatm = True
        if "ab sun" in stripped_line_lower and "{" in stripped_line_lower:
            has_main = True

    if not has_namaste:
        print("Error: Abe lawde! Sanskar bhool gaya? Pehle 'Namaste' likh!")
        return
        
    if not has_main:
        print("Error: Abe bkl! Main logic kahan daalega? 'ab sun {' lagana zaroori hai!")
        return

    if not has_khatm:
        print("Error: Abe bhadwe programme toh khatam kar! Last mein 'Khatm, tata, goodbye' likh!")
        return

    # --- PRE-PROCESSING PASS ---
    for i, line in enumerate(lines):
        line = line.strip()
        
        if "@@" in line:
            line = line.split("@@")[0].strip()
            if not line:
                continue

        if line.endswith("{"):
            stack.append(i)
            # Function definitions bhi lower case pe check kar sakte hain, par variables ke liye original theek hai
            if line.lower().startswith("abe saale"):
                match = re.search(r'(?i)abe saale\s+(\w+)\s*\((.*?)\)\s*\{', line)
                if match:
                    func_name = match.group(1)
                    params = [p.strip() for p in match.group(2).split(',') if p.strip()]
                    functions[func_name] = {'params': params, 'start': i}
        elif line.lower().startswith("} varna {"):
            if stack:
                start = stack.pop()
                jumps[start] = i
                stack.append(i)
        elif line == "}":
            if stack:
                start = stack.pop()
                jumps[start] = i
                jumps[i] = start

    print("--- Lodu Code run ho raha hai... jalwa hai bhai ka! ---\n")

    inside_main = False
    i = 0 

    while i < len(lines):
        line = lines[i].strip()
        line_lower = line.lower() # Case insensitive comparison ke liye

        if "@@" in line:
            line = line.split("@@")[0].strip()
            line_lower = line.lower()

        if not line:
            i += 1
            continue

        # Case Insensitive Start/End Checks
        if "namaste" in line_lower:
            i += 1
            continue
            
        if "ab sun" in line_lower and "{" in line_lower:
            inside_main = True 
            i += 1
            continue

        if "khatm, tata, goodbye" in line_lower:
            break

        if inside_main:
            
            if line_lower.startswith("sabar kar"):
                match = re.search(r'(?i)sabar kar\s*\((.*?)\)', line)
                if match:
                    try:
                        sec = float(eval(match.group(1), desi_globals, variables))
                        time.sleep(sec)
                    except Exception as e:
                        pass
                i += 1
                continue

            if line_lower.startswith("abe saale"):
                i = jumps[i] + 1 
                continue
            
            elif line_lower.startswith("wapas aa"):
                # Case insensitive replace workaround
                expr = re.sub(r'(?i)^wapas aa', '', line).strip()
                try:
                    return_value = eval(expr, desi_globals, variables)
                except:
                    return_value = None
                    
                if call_stack:
                    return_info = call_stack.pop()
                    i = return_info['return_to']
                    if return_info['assign_to']:
                        variables[return_info['assign_to']] = return_value
                    continue

            func_call_match = re.search(r'(\w+)\s*\((.*?)\)', line)
            is_function_call = False
            
            if func_call_match and func_call_match.group(1) in functions:
                func_name = func_call_match.group(1)
                if not line_lower.startswith("abe saale") and not line_lower.startswith("mkc ab print") and not line_lower.startswith("chl ab print"):
                    is_function_call = True
                    args_str = func_call_match.group(2)
                    
                    assign_to = None
                    if line_lower.startswith("bkl"):
                        assign_match = re.search(r'(?i)bkl\s+(\w+)\s*=', line)
                        if assign_match:
                            assign_to = assign_match.group(1)

                    args = []
                    if args_str.strip():
                        arg_exprs = [arg.strip() for arg in args_str.split(',')]
                        for arg_expr in arg_exprs:
                            try:
                                args.append(eval(arg_expr, desi_globals, variables))
                            except:
                                args.append(0)

                    func_def = functions[func_name]
                    for param, arg in zip(func_def['params'], args):
                        variables[param] = arg

                    call_stack.append({
                        'return_to': i + 1,
                        'assign_to': assign_to
                    })
                    i = func_def['start'] + 1
                    continue

            if is_function_call:
                continue

            if line_lower.startswith("jab tak"):
                match = re.search(r'(?i)jab tak\s*\((.*?)\)\s*\{', line)
                if match:
                    try:
                        condition_met = bool(eval(match.group(1), desi_globals, variables))
                    except:
                        condition_met = False
                    if condition_met:
                        i += 1 
                    else:
                        i = jumps[i] + 1 
                else:
                    i += 1
                continue

            elif line_lower.startswith("agar"):
                match = re.search(r'(?i)agar\s*\((.*?)\)\s*\{', line)
                if match:
                    try:
                        condition_met = bool(eval(match.group(1), desi_globals, variables))
                    except:
                        condition_met = False
                    if condition_met:
                        i += 1
                    else:
                        i = jumps[i] + 1
                else:
                    i += 1
                continue

            elif line_lower.startswith("} varna {"):
                i = jumps[i] + 1
                continue

            elif line_lower == "}":
                start_idx = jumps.get(i)
                if start_idx is not None:
                    start_line_lower = lines[start_idx].strip().lower()
                    if start_line_lower.startswith("jab tak"):
                        i = start_idx
                    elif start_line_lower.startswith("abe saale"):
                        if call_stack:
                            return_info = call_stack.pop()
                            i = return_info['return_to']
                            continue
                        else:
                            i += 1
                    elif start_line_lower.startswith("ab sun"):
                        inside_main = False
                        i += 1
                    else:
                        i += 1 
                else:
                    i += 1
                continue

            elif line_lower.startswith("bkl"):
                # Removing "bkl " case-insensitively using regex
                statement = re.sub(r'(?i)^bkl\s+', '', line).strip()
                if "=" in statement:
                    var_name, expression = statement.split("=", 1)
                    var_name = var_name.strip()
                    expression = expression.strip()

                    if "input(" in expression and "bsdk input daal" not in expression.lower():
                        print(f"Error at line {i+1}: Abe asli Lodu Code likh! Python ka input mat chura!")
                        break

                    if "bsdk input daal" in expression.lower():
                        match = re.search(r'(?i)bsdk input daal\s*\((.*?)\)', expression)
                        if match:
                            prompt_text = match.group(1).strip()
                            if len(prompt_text) >= 2 and prompt_text[0] in ['"', "'"] and prompt_text[-1] in ['"', "'"]:
                                prompt_text = prompt_text[1:-1]
                            user_in = input(prompt_text + " ")
                            expression = expression.replace(match.group(0), f'"{user_in}"' if not user_in.isdigit() else str(user_in))

                    expression = re.sub(r'(?i)jhund', '', expression)

                    try:
                        variables[var_name] = eval(expression, desi_globals, variables)
                    except Exception as e:
                        pass
                i += 1
                continue

            elif line_lower.startswith("mkc ab print kar") or line_lower.startswith("chl ab print kar"):
                prefix_pattern = r'(?i)^(mkc ab print kar|chl ab print kar)'
                content = re.sub(prefix_pattern, '', line, count=1).strip()
                
                try:
                    match = re.search(r'\((.*)\)', content)
                    if match:
                        inside_brackets = match.group(1)
                        result = eval(inside_brackets, desi_globals, variables)
                        if isinstance(result, tuple):
                            print(*result)
                        else:
                            print(result)
                    else:
                        result = eval(content, desi_globals, variables)
                        print(result)
                except Exception as e:
                    pass
                i += 1
                continue

        i += 1

def main():
    if len(sys.argv) < 2:
        print("Abe madherboard, file ka naam kaun dega? Aise likh: lodu tera_code.lodu")
    else:
        file_name = sys.argv[1]
        if not file_name.endswith(".lodu"):
            print("Bhai, yahan sirf '.lodu' extension wali file chalegi, andu gandu file nahi!")
        else:
            try:
                with open(file_name, 'r') as file:
                    code = file.read()
                lodu_interpreter(code)
            except FileNotFoundError:
                print(f"Are bhai! '{file_name}' na toh yahan mili. Sahi path aur naam daal.")

if __name__ == "__main__":
    main()