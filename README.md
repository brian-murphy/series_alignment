# series_alignment
Tool for aligning two series visually

## Installation
To install this software, first clone it to your computer.

Next, install it using pip:
```
python -m pip install .
```

Alternatively, you can run the main file using the python command, located at `/series_alignment/series_alignment.py`.

## Usage
### startup
To use the software, you need to provide it with two columns csv files of iri data. The command format is:
```
series_alignment file1.csv[col] file2.csv[col]
```
`col` can be the name of the csv column or the index of the column in the file. The first argument is the 
series you want in the background, and the second arg is the series you want to scale and shift. Here is an example:
```
series_alignment file1.csv[1] file1.csv[HRI]
```
Note that the two columns came from the same file. This is acceptible.
### controls
When you open the application, you will see a graph of the two series.

When you click and drag while holding space, you will shift the series right or left.

When you click and hold the alt key, you will scale the series up or down.

The amount that you scaled and moved the series will be displayed at the top of the
graph.
