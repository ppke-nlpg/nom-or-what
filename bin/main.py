#!/usr/bin/env python
# coding: utf-8

# In[3]:


# setting up the environment

import re
import yaml

from nomorwhat import *

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

macro_config_file = 'macros.yml'
input_file = 'nezzuk.txt'
output_file = 'lassuk.txt'


# In[4]:


# reading macros
with open(macro_config_file, 'r') as fin:
    macros = yaml.load(fin)


# In[5]:


with open(input_file, 'r') as inp, open(output_file, 'w') as outp:
    for i, line in enumerate(inp, start = 1):
        new_sent, to_write = nom_or_what(line, macros)
        write_to_annot_file(new_sent, to_write, outp, i)


# In[ ]:




