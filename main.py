#!/usr/bin/env python
# coding: utf-8

import re
import yaml

from nomorwhat import *

macro_config_file = 'macros.yml'
input_file = 'input_1000.txt'
output_file = 'output_1000.txt'

# reading macros
with open(macro_config_file, 'r') as fin:
    macros = yaml.load(fin, Loader=yaml.FullLoader)

with open(input_file, 'r') as inp, open(output_file, 'w') as outp:
    for i, line in enumerate(inp, start = 1):
        new_sent, to_write = nom_or_what(line, macros)
        write_to_annot_file(new_sent, to_write, outp, i)

