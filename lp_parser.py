'''
Created on Mar 12, 2019

@author: Apostolis Tselios
'''

import re
import os

# REGULAR EXPRESSIONS
minmax_regex = re.compile(r'\A(min|max)', re.I)
objective_function_regex = re.compile(
    r'((\-|\+)?(\d*|\d+\.\d+)?x\d+)((\-|\+)(\d*|\d+\.\d+)?x\d+)+$', re.I)
st_regex = re.compile(r'\A(st|s\.t\.|subjectto)', re.I)
tech_contraints_regex = re.compile(
    r'((\-|\+)?(\d*|\d+\.\d+)?x\d+)((\-|\+)(\d*|\d+\.\d+)?x\d+)+(>=|<=|=)\-?\d+$', re.I)


def load_linear_problem():
    """ Return data

    Loads the linear problem from a file and return its data stripped,
    lowercased and with no spaces.
    """

    data = []
    with open(r'.\txt_files\lp.txt', 'r') as input_file:
        raw_data = input_file.readlines()
        for line in raw_data:
            if line != '\n':
                data.append(line.strip('\n').replace(' ', '').lower())

    print(data)

    return data


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
        print(x_factors)
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
    if match.group() == 'min':
        return -1
    else:
        return 1


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


def filter_nones(matrix):
    """ Return matrix

    Replaces the None elements of an list with 0s.
    """

    for i, element in enumerate(matrix):
        if element == None:
            matrix[i] = 0

    return matrix


def extract_factors(linear_eq, n):
    """ Return factors

    Extracts the factors of the x variables from a right hand side
    of a linear equation.
    """

    # A list with tuples containing the sign and factor of each x.
    # e.g. [('', '23.1'), ('-', '0'), ('+', '23'), ('-', '10')]
    x_factors = re.findall(r'(\-|\+)?(\d+|\d+\.\d+)?x(\d+)', linear_eq)

    # Initialize factors with a list with n None elements
    factors = [None for _ in range(n)]

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
        # Else if there is no sign or the sign is '-' and the value is '0'
        # The factor is the value.
        elif sign == '' and value != '':
            # Try casting to an int. If ValueError cast to a float.
            try:
                factors[pointer - 1] = int(value)
            except ValueError:
                factors[pointer - 1] = float(value)
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

    print('filtered factors:', filter_nones(factors))
    return filter_nones(factors)


def extract_constraints(constraints):
    """ Return eqin

    Eqin is a list containing the type of the constraints e.g. <= .
    """

    eqin = []

    # Iterate over the constraints.
    for constraint in constraints:
        # Constraint type is a match object containing the type of the constraint.
        c_type = re.search(r'<=|>=|=', constraint)
        if c_type.group() == '<=':
            eqin.append(-1)
        elif c_type.group() == '>=':
            eqin.append(1)
        else:
            eqin.append(0)

    return eqin


def extract_bconstants(constraints):
    """ Return b

    Extracts the left hand side constants of a linear equation.
    """

    b = []

    # Iterate over the constraints
    for constraint in constraints:
        match = re.search(r'<=\-?\d+|>=\-?\d+|=\-?\d+', constraint)
        # If the type of the constraint is '>=' or '<=' slice
        # the first 2 elements of the string to get the constant.
        if match.group()[0] == '>' or match.group()[0] == '<':
            b.append(int(match.group()[2:]))
        # Else slice only the first element of the string to get the constant.
        else:
            b.append(int(match.group()[1:]))

    return b


def save_matrixes_to_file(minmax, c, A, b, eqin):
    """
    Save the extracted matrixes to a file called lp_matrixes.txt.
    """

    print(r'Saving to .\files\lp_matrixes.txt ...')

    with open(r'.\txt_files\lp_matrixes.txt', 'w') as output_file:
        if minmax == 1:
            output_file.write('max ')
        else:
            output_file.write('min ')

        print('c =', c, file=output_file)
        i = 0
        print('A =', A[i], file=output_file)
        for i in range(1, len(A)):
            print(f'\t{A[i]}', file=output_file)

        print('eqin =', eqin, file=output_file)
        print('b =', b, file=output_file)

    print('Done!')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the terminal

    minmax = 0  # 1 -> maximize lp / -1 -> minimize lp
    A = []  # matrix factors of the constraints
    b = []  # right hand side of the constraints
    c = []  # factors of the objective function
    Eqin = []  # constraints:-1 (<=), 1 (>=), 0 (=)

    data = load_linear_problem()
    check_format(data)

    n = get_n(data)

    print('Extracting...')
    minmax = get_lp_type(data[0])

    c = extract_factors(data[0][3:], n)

    for constraint in data[1:]:
        if st_regex.match(constraint):
            st_len = get_st_len(constraint)
            A.append(extract_factors(constraint[st_len:], n))
        else:
            A.append(extract_factors(constraint, n))

    Eqin = extract_constraints(data[1:])
    b = extract_bconstants(data[1:])

    save_matrixes_to_file(minmax, c, A, b, Eqin)


if __name__ == '__main__':
    main()
