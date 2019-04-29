'''
Created on Mar 12, 2019

@author: Apostolis Tselios
'''

import re
import os
import argparse

# REGULAR EXPRESSIONS
minmax_regex = re.compile(r'\A(min|max)', re.I)
st_regex = re.compile(r'\A(st|s\.t\.|subjectto)', re.I)

obj_fun_pattern = r'((\-|\+)?(\d*|\d+\.\d+)?x\d+)((\-|\+)(\d*|\d+\.\d+)?x\d+)+$'
objective_function_regex = re.compile(obj_fun_pattern, re.I)

tech_constraints_pattern = r'((\-|\+)?(\d*|\d+\.\d+)?x\d+)((\-|\+)(\d*|\d+\.\d+)?x\d+)+(>=|<=|=)\-?(\d+|\d+\.\d+)$'
tech_contraints_regex = re.compile(tech_constraints_pattern, re.I)


def parse_arguments():
    """ Returns args.input, args.output

    Parses the command line arguments if there are any and returns them.
    """

    parser = argparse.ArgumentParser(
        description='A script that extracts the matrixes of a linear problem.')
    parser.add_argument('-i', '--input', type=str, default=r'./lp_files/lp.txt',
                        help='Name of the input file. Default="./lp_files/lp.txt"')
    parser.add_argument('-o', '--output', type=str, default=r'./lp_files/output_matrixes.txt',
                        help='Name of the output file. Default="./lp_files/output_matrixes.txt"')

    args = parser.parse_args()

    return args.input, args.output


def load_linear_problem(input_file):
    """ Return data

    Loads the linear problem from a file and return its data stripped,
    lowercased and with no spaces.
    """

    data = []
    with open(input_file, 'r') as file:
        raw_data = file.readlines()
        for line in raw_data:
            if line != '\n':
                data.append(line.strip('\n').replace(' ', '').lower())

    print(data)

    return data


def check_for_duplicates(lp):
    """ Checks for duplicate x variables in the same line.
    Raises Exception if it finds a duplicate.
    """
    pattern = r'(\-|\+)?(\d+|\d+\.\d+)?x(\d+)'

    for line in lp:
        if minmax_regex.match(line):
            x_factors = re.findall(pattern, line[3:])
        else:
            x_factors = re.findall(pattern, line)

        prev_pointer = -1
        for factor in x_factors:
            _, _, pointer = factor

            try:
                if int(pointer) == prev_pointer:
                    raise Exception(f'ERROR: Duplicate x in: {line}')
            except Exception as e:
                print(e)
                exit(1)

            prev_pointer = int(pointer)


def check_format(data):
    """ Checks the format of the linear problem and raises Exceptions
    if any errors occur.
    """

    try:
        if not minmax_regex.match(data[0]):
            raise Exception(
                'ERROR: Linear Problem type is not valid.\nTry adding min/max in front of the objective function.')

        if not objective_function_regex.match(data[0][3:]):
            raise Exception(
                'ERROR: Objective function is not valid\nTry this form: max 3x1 + 3x2')

        if not st_regex.match(data[1]):
            raise Exception(
                'ERROR: Subject to keyword is not valid\nTry this form: subject to/s.t./st 3x1 + 3x2 >= 2')
        else:
            st_len = get_st_len(data[1])

        for constraint in data[1:]:
            if st_regex.match(constraint):
                if not tech_contraints_regex.match(constraint[st_len:]):
                    raise Exception(
                        f'ERROR: Constraint -> "{constraint}" is not valid\nTry this form: 3x1 + 3x2 >= 2')
            elif not tech_contraints_regex.match(constraint):
                raise Exception(
                    f'ERROR: Constraint -> "{constraint}" is not valid\nTry this form: 3x1 + 3x2 >= 2')

        check_for_duplicates(data)

    except Exception as e:
        print(e)
        exit(1)


def get_n(data):
    """ Return max_pointer

    Finds and returns the number of x variables in the linear problem.
    """

    max_pointer = 0

    for line in data:
        x_factors = re.findall(r'x\d+', line)
        for factor in x_factors:
            pointer = factor.strip('x')
            if int(pointer) > max_pointer:
                max_pointer = int(pointer)

    return max_pointer


def get_lp_type(obj_fun):
    """ Return 1 or -1

    The type of the linear problem is represented as an
    integer 1 for max , -1 for min.
    """

    match = minmax_regex.match(obj_fun)
    return -1 if match.group() == 'min' else 1


def get_st_len(st_line):
    """Return len(match.group())

    Calculates the length of the 'subject to' keyword depending
    on how it is written.
    """

    match = st_regex.match(st_line)
    if match.group() == 'st':
        return len(match.group())
    elif match.group() == 's.t.':
        return len(match.group())
    else:
        return len(match.group())


def extract_factors(linear_eq, n):
    """ Return factors

    Extracts the factors of the x variables from a right hand side
    of a linear equation.
    """

    # A list with tuples containing the sign, factor and the pointer of each x.
    # e.g. [('', '5.15', '2'), ('-', '', '4')]
    pattern = r'(\-|\+)?(\d+|\d+\.\d+)?x(\d+)'
    x_factors = re.findall(pattern, linear_eq)

    # Initialize factors with a list with n 0 elements.
    factors = [0 for _ in range(n)]

    # Iterate every tuple in x_factors.
    for factor in x_factors:
        # Unpack its sign, its value and its pointer.
        sign, value, str_pointer = factor
        pointer = int(str_pointer)

        # If there is no sign and no value or there is a '+' sign and no value
        # the factor is 1.
        if (sign == '' and value == '') or (sign == '+' and value == ''):
            factors[pointer - 1] = 1
        # Else if there is a '-' sign and no value the factor is -1.
        elif sign == '-' and value == '':
            factors[pointer - 1] = -1
        # Else if there is a '-' sign and some value the factor is negative.
        elif sign == '-' and value != '':
            # Try casting to an int. If ValueError cast to a float.
            try:
                factors[pointer - 1] = int(sign + value)
            except ValueError:
                factors[pointer - 1] = float(sign + value)
        else:
            # Try casting to an int. If ValueError cast to a float.
            try:
                factors[pointer - 1] = int(value)
            except ValueError:
                factors[pointer - 1] = float(value)

    print('Factors:', factors)
    return factors


def extract_constraints(constraints):
    """ Return eqin

    Eqin is a list containing the type of the constraints e.g. <= .
    """

    Eqin = []

    for constraint in constraints:
        match = re.search(r'<=|>=|=', constraint)
        if match.group() == '<=':
            Eqin.append(-1)
        elif match.group() == '>=':
            Eqin.append(1)
        else:
            Eqin.append(0)

    return Eqin


def extract_bconstants(constraints):
    """ Return b

    Extracts the left hand side constants of a linear equation.
    """

    b = []
    pattern = r'>=\-?(\d+|\d+\.\d+)$|<=\-?(\d+|\d+\.\d+)$|=\-?(\d+|\d+\.\d+)$'

    # Iterate over the constraints
    for constraint in constraints:
        match = re.search(pattern, constraint)
        # If the type of the constraint is '>=' or '<=' slice
        # the first 2 elements of the string to get the constant.
        if match.group()[0] == '>' or match.group()[0] == '<':
            try:
                b.append(int(match.group()[2:]))
            except ValueError:
                b.append(float(match.group()[2:]))
        # Else slice only the first element of the string to get the constant.
        else:
            try:
                b.append(int(match.group()[1:]))
            except ValueError:
                b.append(float(match.group()[1:]))

    return b


def save_matrixes_to_file(minmax, c, A, b, eqin, output_file):
    """
    Save the extracted matrixes to a file called lp_matrixes.txt.
    """

    print(r'Saving to ' + output_file)

    with open(output_file, 'w') as file:
        if minmax == 1:
            file.write('max ')
        else:
            file.write('min ')

        print('c =', c, file=file)
        i = 0
        print('A =', A[i], file=file)
        for i in range(1, len(A)):
            print(f'\t{A[i]}', file=file)

        print('Eqin =', eqin, file=file)
        print('b =', b, file=file)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the terminal

    # Parsing command line arguments.
    input_file, output_file = parse_arguments()

    data = load_linear_problem(input_file)
    check_format(data)
    print('Correct format!')

    # 1 -> maximize lp / -1 -> minimize lp
    minmax = get_lp_type(data[0])

    # Number of x variables in the problem
    n = get_n(data)

    print('Extracting from ' + input_file)

    # c: factors of the objective function
    c = extract_factors(data[0][3:], n)

    # A: matrix with the factors of the constraints
    A = []
    for constraint in data[1:]:
        A.append(extract_factors(constraint, n))

    # Eqin: constraints:-1 (<=), 1 (>=), 0 (=)
    Eqin = extract_constraints(data[1:])

    # b: right hand side of the constraints
    b = extract_bconstants(data[1:])

    save_matrixes_to_file(minmax, c, A, b, Eqin, output_file)


if __name__ == '__main__':
    main()
