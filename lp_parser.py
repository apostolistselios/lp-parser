import re
import os

# REGULAR EXPRESSIONS
minmax_regex = re.compile('\A(min|max)', re.I)
objective_function_regex = re.compile(
    '(max|min)([\-|\+]?\d*x\d+)([\-|\+]{1}\d*x\d+)+$', re.I)
subject_to_regex = re.compile(
    '(st|s\.t\.|subjectto)([\-|\+]?\d*x\d+)(([\-|\+]{1}\d*x\d+)+)((>=)|(<=)|(=))(\d+)$', re.I)
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


def extract_obj_fun_factors(obj_fun):
    """ Return factors

    Extract the factors of the x variables from the objective function.
    """

    factors = []
    i = 0

    # Iterate char by char the objective function.
    for char in obj_fun:

        # If the char is not in the following list.
        if char not in ['+', '-', 'x']:

            # If the previous char is equal to '-' concat it with the current char.
            if obj_fun[i - 1] == '-':
                factors.append('-' + char)

            # Else if the previous char is not equal to 'x' it will be equal
            # to '+' so we don't have to concat sth to the factor.
            elif not obj_fun[i - 1] == 'x':
                factors.append(char)

            # Else if the previous char is equal to 'x' the current char
            # is a number after the 'x'.
            elif obj_fun[i - 1] == 'x':
                # If two positions back is either a '-' or a '+' this means
                # that the factor of that x variable is either '-1' or '1'.
                if obj_fun[i - 2] == '-':
                    factors.append('-1')
                elif obj_fun[i - 2] == '+':
                    factors.append('1')

        # Else if its the first char and is not '-'.
        elif i == 0 and not obj_fun[i] == '-':
            factors.append('1')

        i += 1

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

    c = extract_obj_fun_factors(data[0][3:])
    print(c)


if __name__ == '__main__':
    main()
