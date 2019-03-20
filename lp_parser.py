import re
import os

# REGULAR EXPRESSIONS
minmax_regex = re.compile(r'\A(min|max)', re.I)
objective_function_regex = re.compile(
    r'(max|min)([\-|\+]?\d*x\d+)([\-|\+]{1}\d*x\d+)+$', re.I)
subject_to_regex = re.compile(
    r'(st|s\.t\.|subjectto)([\-|\+]?\d*x\d+)(([\-|\+]{1}\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)
tech_contraints_regex = re.compile(
    r'([\-|\+]?\d*x\d+)(([\-|\+]{1}\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)


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
        if not minmax_regex.match(data[0]):
            raise Exception(
                'ERROR: Linear Problem type is not valid.\nTry adding min/max in front of the objective function.')

        if not objective_function_regex.match(data[0]):
            raise Exception(
                'ERROR: Objective function is not valid\nTry this form: max 3x1 + 3x2')

        if not subject_to_regex.match(data[1]):
            raise Exception(
                'ERROR: Subject to keyword is not valid\nTry this form: subject to/s.t./st 3x1 + 3x2 >= 2')

        for constraint in data[2:]:
            if not tech_contraints_regex.match(constraint):
                raise Exception(
                    f'ERROR: Constraint -> "{constraint}" is not valid\nTry this form: 3x1 + 3x2 >= 2')

    except Exception as e:
        print(e)
        exit(1)


def get_lp_type(obj_fun):
    """ Return minmax

    Min max represents the type of the linear problem.
    -1 for min / 1 for max
    """

    match = minmax_regex.match(obj_fun)
    if match.group() == 'min':
        minmax = -1
    else:
        minmax = 1

    return minmax


def extract_factors(linear_eq):
    """ Return factors

    Extract the factors of the x variables from a right hand side
    of a linear equation.
    """

    # A list with each x, its factor and its pointer e.g. -23x1
    x_vars = re.findall(r'([\-|\+]?\d*x\d+)', linear_eq)
    print('x:', x_vars)

    factors = []

    # Iterate element of x_vars.
    for element in x_vars:
        # Partition each element at 'x'. It return 3 values the
        # factor, x, and its pointer. I keep the factor the other
        # two values are not needed.
        factor, *not_needed = element.partition('x')

        # If the factor is a number with a '+' strip the '+' and append it.
        if re.match(r'\+\d*', factor):
            factors.append(factor.strip('+'))
        # Else if the factor is '+' or an empty string the factor is 1.
        elif factor in ['+', '']:
            factors.append('1')
        # Else if the factor is '-0' append 0.
        elif factor == '-0':
            factors.append('0')
        # Else if the factor is '-' the factor is -1.
        elif factor == '-':
            factors.append('-1')
        # Else the factor is a negative number apart from -1.
        else:
            factors.append(factor)

    return factors


def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # clears the terminal

    minmax = 0  # 1 -> maximize lp / -1 -> minimize lp
    A = []  # matrix factors of the constraints
    b = []  # right hand side of the constraints
    c = []  # factors of the objective function
    Eqin = []  # constraints:-1 (<=), 1 (>=), 0 (=)

    data = load_data()
    check_format(data)
    minmax = get_lp_type(data[0])

    c = extract_factors(data[0][3:])
    print(c)


if __name__ == '__main__':
    main()
