import re
import os

# REGULAR EXPRESSIONS
minmax_regex = re.compile(r'\A(min|max)', re.I)
objective_function_regex = re.compile(
    r'((\-|\+)?(\d*|\d+\.\d+)x\d+)((\-|\+)(\d*|\d+\.\d+)x\d+)+$', re.I)
st_regex = re.compile(r'\A(st|s\.t\.|subjectto)', re.I)
tech_contraints_regex = re.compile(
    r'((\-|\+)?(\d*|\d+\.\d+)x\d+)((\-|\+)(\d*|\d+\.\d+)x\d+)+(>=|<=|=)\d+$', re.I)


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


def extract_factors(linear_eq):
    """ Return factors

    Extracts the factors of the x variables from a right hand side
    of a linear equation.
    """

    # A list with tuples containing the sign and factor of each x.
    # e.g. [('', '23.1'), ('-', '0'), ('+', '23'), ('-', '10')]
    x_factors = re.findall(r'(\-|\+)?(\d+|\d+\.\d+)x\d+', linear_eq)
    print('x:', x_factors)

    factors = []

    # Iterate every tuple in x_factors.
    for factor in x_factors:
        # Unpack its sign and its value.
        sign, value = factor
        # If there is no sign and no value or there is a '+' sign and no value
        # the factor is 1.
        if (sign == None and value == None) or (sign == '+' and value == None):
            factors.append('1')
        # Else if there is a '-' sign and no value the factor is -1.
        elif sign == '-' and value == None:
            factors.append('-1')
        # Else if there is no sign or the sign is '-' and the value is '0'
        # The factor is the value.
        elif (sign == None and value != None) or (sign == '-' and value == '0'):
            factors.append(value)
        else:
            factors.append(value)

    return factors


def extract_constraints():
    pass


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
