import re
import os
import numpy as np

# REGULAR EXPRESSIONS
minmax_regex = re.compile('\A(min|max)', re.I)
objective_function_regex = re.compile(
    '(max|min)([\-|\+]?\d*x\d+)([\-|\+]{1}\d*x\d+)+$', re.I)
subject_to_regex = re.compile(
    '(st|s.t.|subjectto)([\-|\+]?\d*x\d+)(([\-|\+]{1}\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)
tech_contraints_regex = re.compile(
    '([\-|\+]?\d*x\d+)(([\-|\+]{1}\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)


def load_data():
    """ Return data

    Loads the linear problem from a file and return its data stripped,
    lowercased and with no spaces.
    """

    data = []
    with open('lp.txt', 'r') as input_file:
        raw_data = input_file.readlines()
        for line in raw_data:
            if line != '\n':
                data.append(line.strip('\n').replace(' ', '').lower())

    print(raw_data)
    print(data)

    return data


def check_format(data):
    """ Checks the format of the linear problem and raises Exceptions
    if any errors occur.
    """

    try:
        if minmax_regex.match(data[0]):
            lp_type = minmax_regex.match(data[0]).group()
            print(lp_type)
        else:
            raise Exception(
                'ERROR: Linear Problem type is not valid.\nTry adding min/max in front of the objective function.')

        if objective_function_regex.match(data[0]):
            obj_fun = objective_function_regex.match(data[0]).group()
            print(obj_fun)
        else:
            raise Exception(
                'ERROR: Objective function is not valid\nTry this form: max 3x1 + 3x2')

        if subject_to_regex.match(data[1]):
            st = subject_to_regex.match(data[1]).group()
            print(st)
        else:
            raise Exception(
                'ERROR: Subject to keyword is not valid\nTry this form: subject to/s.t./st 3x1 + 3x2 >= 2')

        for constraint in data[2:]:
            if tech_contraints_regex.match(constraint):
                print(constraint)
            else:
                raise Exception(
                    f'ERROR: Constraint -> "{constraint}" is not valid\nTry this form: 3x1 + 3x2 >= 2')

    except Exception as e:
        print(e)
        exit(1)


def extract_obj_fun_factors(objective_function):
    print(objective_function)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')    # clears the terminal

    # # matrix factors of the constraints
    # A = np.empty((m, n), dtype=np.int32)
    #
    # # right hand side of the constraints
    # b = np.empty((1, m), dtype=np.int32)
    #
    # # factors of the objective function
    # c = np.empty((1, n), dtype=np.int32)
    #
    # # constraints:-1 (<=), 1 (>=), 0 (=)
    # Eqin = np.empty((1, m), dtype=np.int8)

    data = load_data()
    check_format(data)

    n = 0   # x variables
    m = 0   # technological constraints
    minmax = 0  # 1 -> maximize lp / -1 -> minimize lp

    match = minmax_regex.match(data[0])
    if match.group() == 'min':
        minmax = -1
    else:
        minmax = 1

    print(minmax)

    c = extract_obj_fun_factors(data[0][3:])


if __name__ == '__main__':
    main()
