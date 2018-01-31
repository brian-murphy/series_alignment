import re
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from patch_navbar import NavBarPatcher

TARGET_KEY = " "  # space key

def align(csv_selector1, csv_selector2):
    (file_name1, col_name1) = parse_file_name_and_col(csv_selector1)
    (file_name2, col_name2) = parse_file_name_and_col(csv_selector2)

    df1 = pd.read_csv(file_name1, usecols=[col_name1])
    df2 = pd.read_csv(file_name2, usecols=[col_name2])

    array = df1.join(df2, how="outer").as_matrix()

    axes = plt.plot(array)

    patcher = NavBarPatcher(axes[1].figure.canvas, TARGET_KEY)
    scaler = Scaler(array, axes, TARGET_KEY)

    plt.show()

def parse_file_name_and_col(csv_selector):
    """parses input arguments"""
    match = re.search("(.*)\[(.*)\]", csv_selector)
    col = int(match.group(2)) if str.isdigit(match.group(2)) else match.group(2)
    return (match.group(1), col)

class Scaler:
    def __init__(self, array, axes, target_key):
        self.array = array
        self.axes = axes
        self.v_isnan = np.vectorize(math.isnan)
        self.start_x = float('nan')
        self.start_y = float('nan')
        self.mouse_down = False
        self.target_key = target_key
        self.target_key_down = False

        self.axes[1].figure.canvas.mpl_connect('button_press_event', self.on_mouse_down)
        self.axes[1].figure.canvas.mpl_connect('button_release_event', self.on_mouse_up)
        self.axes[1].figure.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.axes[1].figure.canvas.mpl_connect('key_press_event', self.on_key_down)
        self.axes[1].figure.canvas.mpl_connect('key_release_event', self.on_key_up)

    def on_mouse_down(self, event):
        if self.target_key_down:
            self.start_x = event.x
            self.start_y = event.y
        # y = self.axes[1].get_ydata()
        # y[self.v_isnan(y)] = np.ones((1,))
        # self.axes[1].set_ydata(y)
        # event.canvas.draw()

    def on_mouse_up(self, event):
        print event

    def on_mouse_move(self, event):
        pass

    def on_key_down(self, event):
        if event.key == self.target_key:
            self.target_key_down = True

    def on_key_up(self, event):
        if event.key == self.target_key:
            self.target_key_down = True




if __name__ == "__main__":
    import sys
    align(sys.argv[1], sys.argv[2])
