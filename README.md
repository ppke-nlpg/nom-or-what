# nom-or-what
`Nom-or-what` algorithm, designed to disambiguate suffixless nominals in Hungarian.

## testing

Run
```python
python3 main.py
```
and see output of the algo in `output_1000.txt`.

`nomorwhat.py`: the nom-or-what module. 

`main.py`: for testing nom-or-what.

The input file has to contain one sentence / line.
The tokens need to be annotated with emMorph (in a  "/"-separated format, and with the tag set of emMorph).
`input_1000.txt` is an example file; it contains 1000 sentences nom-or-what has been evaluated on.

The output file will be like `output_1000.txt`: each suffixless nominals are listed with a two-token parsing window and proposed `Nom-or-what` tag (which appears three times for manual annotation purposes).

`macros.yml`: config file for the macros used in nom-or-what.

## evaluation

Run
```python
python3 evaluate.py
```
and see output of the algo in `output_1000.txt`.

`evaluate.py`: for evaluating nom-or-what using `annotated_1000.txt`.

