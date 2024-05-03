from itertools import permutations
import sys

def parse(_line):
    line = _line + '#'
    pos = 0

    def skip(s):
        nonlocal pos
        if line.startswith(s, pos):
            pos += len(s)
            return True
        return False

    def e():
        x = dij()
        if skip('->'):
            right = e()
            return {'type': '->', 'left': x, 'right': right}
        return x

    def dij():
        x = con()
        while skip('|'):
            right = con()
            x = {'type': '|', 'left': x, 'right': right}
        return x

    def con():
        x = nt()
        while skip('&'):
            right = nt()
            x = {'type': '&', 'left': x, 'right': right}
        return x

    def nt():
        nonlocal pos
        if skip('('):
            x = e()
            skip(')')
            return x
        if skip('!'):
            inner = nt()
            return {'type': '!', 'inner': inner}
        x = ''
        while line[pos].isdigit() or line[pos].isalpha() or line[pos] == "'":
            x += line[pos]
            pos += 1
        return {'type': 'var', 'name': x}

    return e()

def is_axiom_1(expr_tree):
    if expr_tree['type'] == '->':
        left_alpha = expr_tree['left']
        right_expr = expr_tree['right']
        if right_expr['type'] == '->':
            middle_expr = right_expr['right']
            if middle_expr == left_alpha:
                return True
    return False

def is_axiom_2(expr_tree):
    if expr_tree['type'] == '->':
        term1 = expr_tree['left']
        right = expr_tree['right']
        if term1['type'] == '->':
            term1_alpha = term1['left']
            term1_betta = term1['right']
            if right['type'] == '->':
                term2 = right['left']
                term3 = right['right']
                if term2['type'] == '->':
                    term2_alpha = term2['left']
                    term2_right = term2['right']
                    if term2_right['type'] == '->':
                        term2_betta = term2_right['left']
                        term2_gamma = term2_right['right']
                        if term3['type'] == '->':
                            term3_alpha = term3['left']
                            term3_gamma = term3['right']
                            if term1_alpha == term2_alpha:
                                if term2_alpha == term3_alpha:
                                    if term1_betta == term2_betta:
                                        if term2_gamma == term3_gamma:
                                            return True
    return False

def is_axiom_3(expr_tree):
    if expr_tree['type'] == '->':
        alpha1 = expr_tree['left']
        right = expr_tree['right']
        if right['type'] == '->':
            betta1 = right['left']
            term3 = right['right']
            if term3['type'] == '&':
                alpha2 = term3['left']
                betta2 = term3['right']
                if alpha1 == alpha2:
                    if betta1 == betta2:
                        return True
    return False
def is_axiom_4(expr_tree):
    if expr_tree['type'] == '->':
        left = expr_tree['left']
        alpha1 = expr_tree['right']
        if left['type'] == '&':
            alpha2 = left['left']
            if alpha1 == alpha2:
                return True
    return False
def is_axiom_5(expr_tree):
    if expr_tree['type'] == '->':
        left = expr_tree['left']
        alpha1 = expr_tree['right']
        if left['type'] == '&':
            alpha2 = left['right']
            if alpha1 == alpha2:
                return True
    return False
def is_axiom_6(expr_tree):
    if expr_tree['type'] == '->':
        alpha1 = expr_tree['left']
        right = expr_tree['right']
        if right['type'] == '|':
            alpha2 = right['left']
            if alpha1 == alpha2:
                return True
    return False
def is_axiom_7(expr_tree):
    if expr_tree['type'] == '->':
        alpha1 = expr_tree['left']
        right = expr_tree['right']
        if right['type'] == '|':
            alpha2 = right['right']
            if alpha1 == alpha2:
                return True
    return False
def is_axiom_8(expr_tree):
    if expr_tree['type'] == '->':
        term1 = expr_tree['left']
        term23 = expr_tree['right']
        if term1['type'] == '->':
            alpha1 = term1['left']
            gamma1 = term1['right']
            if term23['type'] == '->':
                term2 = term23['left']
                term3 = term23['right']
                if term2['type'] == '->':
                    betta2 = term2['left']
                    gamma2 = term2['right']
                    if term3['type'] == '->':
                        left3 = term3['left']
                        gamma3 = term3['right']
                        if left3['type'] == '|':
                            alpha3 = left3['left']
                            betta3 = left3['right']
                            if alpha1 == alpha3:
                                if betta2 == betta3:
                                    if gamma1 == gamma2:
                                        if gamma2 == gamma3:
                                            return True
    return False
def is_axiom_9(expr_tree):
    if expr_tree['type'] == '->':
        term1 = expr_tree['left']
        term23 = expr_tree['right']
        if term1['type'] == '->':
            alpha1 = term1['left']
            betta1 = term1['right']
            if term23['type'] == '->':
                term2 = term23['left']
                term3 = term23['right']
                if term2['type'] == '->':
                    alpha2 = term2['left']
                    neg2 = term2['right']
                    if neg2['type'] == '!':
                        betta2 = neg2['inner']
                        if term3['type'] == '!':
                            alpha3 = term3['inner']
                            if alpha1 == alpha2:
                                if alpha2 == alpha3:
                                    if betta1 == betta2:
                                        return True
    return False
def is_axiom_10(expr_tree):
    if expr_tree['type'] == '->':
        term1 = expr_tree['left']
        alpha2 = expr_tree['right']
        if term1['type'] == '!':
            neg1 = term1['inner']
            if neg1['type'] == '!':
                alpha1 = neg1['inner']
                if alpha1 == alpha2:
                    return True
    return False

def split_context_expression(line):
    parts = line.split("|-")
    if parts[0] == '':
        return [], parts[1]
    return parts[0].split(","), parts[1]

def to_string(expr):
  if expr['type']  == "var":
    return "("+expr["name"] + ")"
  elif expr["type"] == "!":
    return "(!" + to_string(expr["inner"]) + ")"
  elif expr["type"] == "&":
    return "(" + to_string(expr["left"]) + "&" + to_string(expr["right"]) + ")"
  elif expr["type"] == "|":
    return "(" + to_string(expr["left"]) + "|" + to_string(expr["right"]) + ")"
  elif expr["type"] == "->":
    return "(" + to_string(expr["left"]) + "->" + to_string(expr["right"]) + ")"
    

def main():
  #sys.setrecursionlimit(2**30)
  prev = []
  prev_contexts = []
  prev_extended_contexts = []
  prev_shorts = []
  number = 0
  for line in sys.stdin:
    line = line.strip()
    number += 1
    def get_result():
        exp_contexts, exp = split_context_expression(line)
        exp_extended_contexts = [parse(context) for context in exp_contexts]
      
        parsed_exp = parse(exp)
        c = parsed_exp
        while (c['type'] == '->'):
            exp_extended_contexts.append(c['left'])
            c = c['right']
        
        parsed_contexts = [parse(context) for context in exp_contexts]

        res = None
        for i, context in enumerate(exp_contexts):
            if context == exp:
                res = f"[{number}] {line} [Hyp. {i + 1}]"
                break
        if is_axiom_1(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 1]"
        elif is_axiom_2(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 2]"
        elif is_axiom_3(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 3]"
        elif is_axiom_4(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 4]"
        elif is_axiom_5(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 5]"
        elif is_axiom_6(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 6]"
        elif is_axiom_7(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 7]"
        elif is_axiom_8(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 8]"
        elif is_axiom_9(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 9]"
        elif is_axiom_10(parsed_exp):
            res = f"[{number}] {line} [Ax. sch. 10]"
        sorted_exp_extended_contexts = ",".join(sorted(map(to_string, exp_extended_contexts)))
        sorted_exp_contexts = ",".join(sorted(map(to_string, parsed_contexts)))
        if res is None and number > 2:
            candidates = []
            for i in range(len(prev_contexts)):
                if prev_contexts[i] == sorted_exp_contexts:
                  candidates.append(i)
            for i in candidates:
                tree1 = prev[i]
                if tree1['type'] == '->':
                    alpha = tree1['left']
                    betta = tree1['right']
                    if betta == parsed_exp:
                        for j in candidates:
                            tree2 = prev[j]
                            if tree2 == alpha:
                                res = f"[{number}] {line} [M.P. {j+1}, {i+1}]"
                                break
        
        
        if res is None and number > 1:
            for i, prev_extended_context in enumerate(prev_extended_contexts):
                if prev_shorts[i] == c and prev_extended_context == sorted_exp_extended_contexts:
                    res = f"[{number}] {line} [Ded. {i + 1}]"
        
        prev_extended_contexts.append(sorted_exp_extended_contexts)
        prev_contexts.append(sorted_exp_contexts)
        prev.append(parsed_exp)
        prev_shorts.append(c)
        if res is not None: 
          return res
        return f"[{number}] {line} [Incorrect]"
    print(get_result())
        

if __name__ == '__main__':
  main()