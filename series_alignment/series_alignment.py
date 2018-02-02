import re

import pandas as pd
import matplotlib.pyplot as plt

from patch_navbar import NavBarPatcher
from transformer import Transformer

MOVING_KEY = " "  # space key
SCALING_KEY = "alt"

def align(csv_selector1, csv_selector2):
    (file_name1, col_name1) = parse_file_name_and_col(csv_selector1)
    (file_name2, col_name2) = parse_file_name_and_col(csv_selector2)

    df1 = pd.read_csv(file_name1, usecols=[col_name1])
    df2 = pd.read_csv(file_name2, usecols=[col_name2])

    array = df1.join(df2, how="outer").as_matrix()

    axes = plt.plot(array)

    patcher = NavBarPatcher(axes[1].figure.canvas, [MOVING_KEY, SCALING_KEY])
    transformer = Transformer(axes, MOVING_KEY, SCALING_KEY)

    plt.show()

def parse_file_name_and_col(csv_selector):
    """parses input arguments"""
    match = re.search("(.*)\[(.*)\]", csv_selector)
    col = int(match.group(2)) if str.isdigit(match.group(2)) else match.group(2)
    return (match.group(1), col)


if __name__ == "__main__":
    import sys
    align(sys.argv[1], sys.argv[2])
