"""Copyright Brian Murphy, Georgia Tech 2018"""

import re
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def align(csv_selector1, csv_selector2):
    (file_name1, col_name1) = parse_file_name_and_col(csv_selector1)
    (file_name2, col_name2) = parse_file_name_and_col(csv_selector2)

    df1 = pd.read_csv(file_name1, usecols=[col_name1])
    df2 = pd.read_csv(file_name2, usecols=[col_name2])

    array = df1.join(df2, how="outer").as_matrix()

    axes = plt.plot(array)

    scaler = Scaler(array, axes)

    plt.show()

def parse_file_name_and_col(csv_selector):
    """parses input arguments"""
    match = re.search("(.*)\[(.*)\]", csv_selector)
    col = int(match.group(2)) if str.isdigit(match.group(2)) else match.group(2)
    return (match.group(1), col)

class Scaler:
    def __init__(self, array, axes):
        self.array = array
        self.axes = axes
        
        self.axes[1].figure.canvas.mpl_connect('button_press_event', self.onclick)
        # self.axes[1].figure.canvas.mpl_connect('motion_notify_event', self.onmove)

    def onclick(self, event):
        print event

        scaleby = 30000

        y = self.axes[1].get_ydata()

        v_isnan = np.vectorize(math.isnan)

        y[v_isnan(y)] = np.ones((1,))

        self.axes[1].set_ydata(y)

        # event.canvas.draw()

    def onmove(self, event):
        print event

if __name__ == "__main__":
    import sys
    align(sys.argv[1], sys.argv[2])
