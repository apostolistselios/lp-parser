import re
import os
import numpy as np

os.system('cls' if os.name == 'nt' else 'clear')    # clears the terminal

minmax_regex = re.compile('\A(min|max)', re.I)
subject_to_regex = re.compile(
    '(st|s.t.|subject to)(([\-|\+]?\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)
objective_function_regex = re.compile('(max|min)([\-|\+]?\d*x\d+)+$', re.I)
tech_contraints_regex = re.compile(
    '(([\-|\+]?\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)

minmax = 0  # 1 -> maximize lp / -1 -> minimize lp
A = []    # matrix for the factors of the constraints
b = []      # right hand side of the constraints
c = []      # factors of the objective function
Eqin = []   # type of contraint: -1 -> (<=) / 1 -> (>=) / 0 -> (=)

data = []

with open('lp.txt', 'r') as f:
    raw_data = f.readlines()
    for line in raw_data:
        if line != '\n':
            data.append(line.strip('\n').replace(' ', ''))

print(raw_data)
print(data)

if minmax_regex.match(data[0]):
    lp_type = minmax_regex.match(data[0]).group()
    print(lp_type)
else:
    print('Error lp_type')

if objective_function_regex.match(data[0]):
    obj_fun = objective_function_regex.match(data[0]).group()
    print(obj_fun)
else:
    print('Error objective function')

if subject_to_regex.match(data[1]):
    st = subject_to_regex.match(data[1]).group()
    print(st)
else:
    print('Error st')

for constraint in data[2:]:
    if tech_contraints_regex.match(constraint):
        print(constraint)
    else:
        print('Error in constraints: ' + constraint)
