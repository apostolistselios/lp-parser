# Linear Problem Parser

Python Version: 3.7

### Description

- LP Parser
    Parses a given Linear Problem and outputs its matrices in a txt file.

- Dual Converter
    Parses a given Primal Linear Problem and outputs the matrices of its Dual L.P. in a txt file. The input txt file can contain either the Primal L.P. in the format shown below or the matrices of the Primal L.P.. If the input L.P. isn't parsed, like shown below the dual converter will run lp_parser.py and use its output (the matrices of the Primal L.P.) to create the matrices of its Dual L.P..

### Linear Problem Format

The Linear Problem should be written in a txt file like the example below.

    max/min 3x1 - 4x3 + 6x4
    st/s.t./subject to 7x1 + x2 - x3 + 10x4 >= 10
    19x2 + 20x3 - x4 <= 6

### Running the scripts

- lp_parser.py
    Takes 2 command line arguments:
    - `-i`/`--input`: The name of the input file. Default=./lp_files/lp.txt
    - `-o`/`--output`: The name of the output file. Default=./lp_files/output_matrices.txt

    To run the lp_parser script run the following command in your terminal:
    `python lp_parser.py`
    or for example:
    `python lp_parser.py -i ./lp_files/linear_problem.txt -o ./lp_files/output_matrices_1.txt`

    Run this command for help:
    `python lp_parser.py -h`


- dual_converter.py
    Takes 3 command line arguments:
    -`-i`/`--input`: The name of the input file. Default=./lp_files/lp.txt
    -`-o`/`--output`: The name of the output file. Default=./lp_files/output_dual.txt
    -`-p`/`--parsed`: If this command line argument is True the input file is parsed by the lp_parser.py so it contains the matrices of the Primal L.P.. If it's False the input file contains the Primal L.P. in the format shown above. Default=False.

    To run the dual_converter script run the following command in your terminal:
    `python dual_converter.py`
    or for example:
    `python dual_converter.py -i ./lp_files/output_matrices.txt -o ./lp_files/output_dual_1.txt -p True`

    Run this command for help:
    `python dual_converter.py -h`
