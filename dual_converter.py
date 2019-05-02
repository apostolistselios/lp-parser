'''
Created on April 29, 2019

@author: Apostolis Tselios
'''

import os
import re
import argparse
import numpy as np

# REGULAR EXPRESSIONS
element_regex = re.compile(r'\-\d+\.\d+|\d+\.\d+|\-\d+|\d+', re.I)


def parse_arguments():
    """ Parses the command line arguments if there are any and returns them.

    return: args.input, args.output, args.parsed
    """

    parser = argparse.ArgumentParser(
        description='A script that turns the matrices of a Primal Linear Problem to the matrices of a its Dual Linear Problem.')
    parser.add_argument('-i', '--input', type=str, default=r'./lp_files/lp.txt',
                        help='Name of the input file. Default="./lp_files/lp.txt"')
    parser.add_argument('-o', '--output', type=str, default=r'./lp_files/output_dual.txt',
                        help='Name of the output file. Default="./lp_files/output_dual.txt"')
    parser.add_argument('-p', '--parsed', type=bool, default=False,
                        help='Is the input file formed in matrices or is it the raw LP?(True/False) Default=False.')

    args = parser.parse_args()

    return args.input, args.output, args.parsed


def load_data(input):
    """Reads the L.P. from a file and returns the data with no spaces.

    param: input
    return: data
    """

    with open(input, 'r') as f:
        raw_data = f.readlines()

    data = [line.replace(' ', '') for line in raw_data]
    return data


def parse_lp_type(type):
    """Returns the type of the linear problem.

    param: type
    return: 1 or -1
    """
    return 1 if type == 'max' else -1


def parse_elements(line):
    """Parses the elements of a matrix from a string

    params: line
    return: elements
    """
    matches = element_regex.findall(line)
    elements = []
    for e in matches:
        try:
            elements.append(int(e))
        except ValueError:
            elements.append(float(e))

    return elements


def parse_matrices(data):
    """Parses the matrices of a Primal Linear Problem from a string.

    params: data
    return: primal_type, c, A, b, Eqin
    """

    primal_type = parse_lp_type(data[0][:3])
    c = parse_elements(data[0])
    b = parse_elements(data[-1])
    Eqin = parse_elements(data[-2])
    A = [parse_elements(line) for line in data[1:-2]]

    return primal_type, c, A, b, Eqin


def create_dual(primal_type, A, len_b, Eqin):
    """Creates the Dual L.P. of the the Primal L.P. given as input
    and returns the matrices of the Dual L.P.

    params: primal_type,A, len_b, Eqin
    return: dual_type, dual_A, dual_eqin
    """

    dual_type = -1 if primal_type == 1 else 1
    dual_A = np.transpose(np.array(A))

    if dual_type == -1:
        # If the dual_type is -1 (min) the primal was 1 (max) so for
        # positive variables we have >= (1) constraints.
        dual_eqin = [1 for _ in range(len_b)]
    else:
        # If the dual_type is 1 (max) the primal was -1 (min) so for
        # positive variables we have <= (-1) constraints.
        dual_eqin = [-1 for _ in range(len_b)]

    return dual_type, dual_A, dual_eqin


def save_dual_problem(dual_type, c, dual_A, b, dual_eqin, output):
    """Saves the matrices of the Dual L.P. in a file.

    params: dual_type, c, dual_A, b, dual_eqin, output
    """

    print(f'Saving to {output}...')
    with open(output, 'w') as f:
        f.write('min ') if dual_type == -1 else f.write('max ')

        print(f'b = {b}', file=f)
        print(f'A_transpose = {dual_A}', file=f)
        print(f'Dual_Eqin = {dual_eqin}', file=f)
        print(f'c = {c}', file=f)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    input, output, parsed = parse_arguments()

    if parsed:
        data = load_data(input)
    else:
        os.system(
            f'python lp_parser.py -i {input} -o ./lp_files/output_matrices.txt')
        parsed_file = r'./lp_files/output_matrices.txt'
        data = load_data(parsed_file)

    print('Creating Dual Linear Problem...')
    primal_type, c, A, b, Eqin = parse_matrices(data)

    dual_type, dual_A, dual_eqin = create_dual(primal_type, A, len(b), Eqin)

    save_dual_problem(dual_type, c, dual_A, b, dual_eqin, output)


if __name__ == '__main__':
    main()
