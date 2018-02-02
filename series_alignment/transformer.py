"""This module handles the transformations to the data to scale and offset it.
It also interacts with pyplot to dynamically display the results"""

import math

import numpy as np

class Transformer:
    def __init__(self, axes, moving_key, scaling_key):
        self.axes = axes
        self.v_isnan = np.vectorize(math.isnan)
        self.mouse_start_x = float('nan')
        self.mouse_start_y = float('nan')
        self.mouse_down = False
        self.moving_key = moving_key
        self.moving_key_down = False
        self.data_start_index = 0
        self.ydata = self.axes[1].get_ydata()
        self.data_size = np.size(self.ydata) - \
            np.count_nonzero(np.isnan(self.ydata))
        self.scaling_vector = np.zeros(np.size(self.ydata))
        self.scaling_vector[0] = 1

        canvas = self.axes[1].figure.canvas
        canvas.mpl_connect('button_press_event', self.on_mouse_down)
        canvas.mpl_connect('button_release_event', self.on_mouse_up)
        canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        canvas.mpl_connect('key_press_event', self.on_key_down)
        canvas.mpl_connect('key_release_event', self.on_key_up)

    def start_moving(self, xdata, ydata):
        self.mouse_start_x = int(xdata)
        self.mouse_start_y = int(ydata)

    def move(self, event):
        dx = self.calc_dx(event)
        new_y = self.make_scaled_array(1 + (dx / self.data_size))

        self.axes[1].set_ydata(new_y)
        event.canvas.draw()

    def calc_dx(self, event):
        mouse_offset = int(event.xdata) - self.mouse_start_x
        max_dx = np.size(self.ydata) - self.data_size - self.data_start_index
        min_dx = -self.data_start_index
        return max(min(mouse_offset, max_dx), min_dx)

    def make_scaled_array(self, factor):
        """technique found at https://stackoverflow.com/a/29444822/1429640"""
        new_y = np.empty(self.ydata.shape)
        new_y.fill(np.nan)

        current_data = self.ydata[self.data_start_index:
                                  self.data_start_index + self.data_size]

        x = np.arange(0, factor * np.size(current_data), factor)
        xx = np.arange((np.size(current_data) - 1) * factor + 1)
        new_data = np.interp(xx, x, current_data)

        new_y[self.data_start_index:self.data_start_index +
              np.size(new_data)] = new_data
        return new_y

    def make_shifted_array(self, dx):
        new_y = np.empty(self.ydata.shape)
        new_y.fill(np.nan)

        end_index = self.data_start_index + self.data_size

        new_y[self.data_start_index + dx:end_index +
              dx] = self.ydata[self.data_start_index:end_index]
        return new_y

    def stop_moving(self, event):
        dx = self.calc_dx(event)
        new_y = self.make_shifted_array(dx)

        self.ydata = new_y
        self.data_start_index = self.data_start_index + dx
        self.axes[1].set_ydata(self.ydata)
        event.canvas.draw()

    def on_mouse_down(self, event):
        if self.moving_key_down and event.inaxes:
            self.start_moving(event.xdata, event.ydata)
        self.mouse_down = True

    def on_mouse_up(self, event):
        if self.moving_key_down and event.inaxes:
            self.stop_moving(event)
        self.mouse_down = False

    def on_mouse_move(self, event):
        if self.mouse_down and self.moving_key_down and event.inaxes:
            self.move(event)

    def on_key_down(self, event):
        """will be repeated as the key stays held down"""
        if event.key == self.moving_key and not self.moving_key_down:
            if self.mouse_down:
                self.start_moving(event.xdata, event.ydata)
            self.moving_key_down = True

    def on_key_up(self, event):
        if event.key == self.moving_key:
            if self.mouse_down:
                self.stop_moving(event)
            self.moving_key_down = False
