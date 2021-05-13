# nom-or-what
Nom-or-what algorithm, designed to disambiguate case endings on nouns, adjectives, numerals etc. in Hungarian.

nom-or-what.py: the nom-or-what module. 

main.ipynb: a notebook to test nom-or-what.

The input file has to contain one sentence / line. The tokens need to be annotated with emMorph (in a  "/"-separated format, and with the tag set of emMorph).
input_1000.txt is an example file; it contains 1000 sentences nom-or-what has been evaluated on.

The output file will be like output_1000.txt: Enumerated sentences with the parsing window of each suffixless nominals in them, and the proposed tag of each suffixless nominal (listed three times - to prepare the file for the manual annotation).

macros.yml: config file for the macros used in nom-or-what.

evaluate.ipynb: a notebook for the evaluation of files in the format of output_1000.txt and annotated_1000.txt.

