"""This module handles the transformations to the data to scale and offset it.
It also interacts with pyplot to dynamically display the results"""

import math

import numpy as np
import matplotlib.pyplot as plt

class Transformer:
    def __init__(self, axes, moving_key, scaling_key):
        self.axes = axes
        self.v_isnan = np.vectorize(math.isnan)

        self.mouse_start_x = float('nan')
        self.mouse_start_y = float('nan')
        self.data_start_index = 0
        self.ydata = self.axes[1].get_ydata()
        self.original_ydata = self.ydata
        self.data_size = np.size(self.ydata) - \
            np.count_nonzero(np.isnan(self.ydata))
        self.original_data_size = self.data_size
        self.min_factor = 1.0 / self.original_data_size
        self.is_moving = False
        self.is_scaling = False
        
        self.scale_factor = 1.0

        canvas = self.axes[1].figure.canvas
        self.state_machine = StateMachine(canvas, self, moving_key, scaling_key)
        canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def start_moving(self, event):
        self.mouse_start_x = int(event.xdata)
        self.mouse_start_y = int(event.ydata)
        self.is_moving = True

    def move(self, event):
        dx = self.calc_dx_for_moving(event)
        new_y = self.make_shifted_array(dx)
        self.axes[1].set_ydata(new_y)
        event.canvas.draw()

    def calc_dx_for_moving(self, event):
        mouse_offset = int(event.xdata) - self.mouse_start_x
        max_dx = np.size(self.ydata) - self.data_size - self.data_start_index
        min_dx = -self.data_start_index
        return max(min(mouse_offset, max_dx), min_dx)

    def make_shifted_array(self, dx):
        new_y = np.empty(self.ydata.shape)
        new_y.fill(np.nan)

        end_index = self.data_start_index + self.data_size

        new_y[self.data_start_index + dx:end_index +
              dx] = self.ydata[self.data_start_index:end_index]
        return new_y

    def stop_moving(self, event):
        dx = self.calc_dx_for_moving(event)
        new_y = self.make_shifted_array(dx)

        self.ydata = new_y
        self.data_start_index = self.data_start_index + dx
        self.axes[1].set_ydata(self.ydata)
        plt.title("offset:" + str(self.data_start_index) + " scale factor:" + str(round(self.scale_factor, 4)))
        event.canvas.draw()
        self.is_moving = False

    def start_scaling(self, event):
        self.mouse_start_x = int(event.xdata)
        self.mouse_start_y = int(event.ydata)
        self.is_scaling = True

    def scale(self, event):
        (factor, new_size) = self.calc_factor_for_scaling(event)
        new_y = self.make_scaled_array(factor)
        self.axes[1].set_ydata(new_y)
        event.canvas.draw()

    def calc_factor_for_scaling(self, event):
        """calculates that factor to scale the original data by to 
        get a dataset of the desired size. also returns the new size
        of the data set"""
        displacement = int(event.xdata) - self.mouse_start_x

        input_size = max(1, self.data_size + displacement)
        max_size = np.size(self.original_ydata) - self.data_start_index

        new_size = min(input_size, max_size)
        factor = max(self.min_factor, float(new_size) / self.original_data_size)
        return (factor, new_size)

    def make_scaled_array(self, factor):
        """technique found at https://stackoverflow.com/a/29444822/1429640"""
        new_y = np.empty(self.ydata.shape)
        new_y.fill(np.nan)

        original_data = self.original_ydata[:self.original_data_size]

        x = np.arange(0, factor * np.size(original_data), factor)
        xx = np.arange((np.size(original_data) - 1) * factor + 1)
        new_data = np.interp(xx, x, original_data)

        new_y[self.data_start_index:self.data_start_index +
              np.size(new_data)] = new_data
        return new_y

    def stop_scaling(self, event):
        (factor, new_size) = self.calc_factor_for_scaling(event)
        new_y = self.make_scaled_array(factor)

        self.ydata = new_y
        self.data_size = new_size

        self.axes[1].set_ydata(new_y)
        self.scale_factor = factor
        plt.title("offset:" + str(self.data_start_index) +
                  " scale factor:" + str(round(self.scale_factor, 4)))
        event.canvas.draw()

        self.is_scaling = False

    def on_mouse_move(self, event):
        if event.inaxes:
            if self.is_moving:
                self.move(event)
            elif self.is_scaling:
                self.scale(event)


class StateMachine():

    def __init__(self, canvas, transformer, moving_key, scaling_key):
        self.transformer = transformer
        self.moving_key = moving_key
        self.scaling_key = scaling_key
        self.mouse_is_down = False
        self.moving_key_down = False
        self.scaling_key_down = False

        canvas.mpl_connect('key_press_event', self.on_key_down)
        canvas.mpl_connect('key_release_event', self.on_key_up)
        canvas.mpl_connect('button_press_event', self.on_mouse_down)
        canvas.mpl_connect('button_release_event', self.on_mouse_up)
        
    def on_key_down(self, event):
        # key down event repeats
        if event.key == self.moving_key and not self.moving_key_down:
            if self.mouse_is_down and not self.scaling_key_down:
                self.transformer.start_moving(event)
            elif self.mouse_is_down and self.scaling_key_down:
                self.transformer.stop_scaling(event)
            self.moving_key_down = True
        elif event.key == self.scaling_key and not self.scaling_key_down:
            if self.mouse_is_down and not self.moving_key_down:
                self.transformer.start_scaling(event)
            elif self.mouse_is_down and self.moving_key_down:
                self.transformer.stop_moving(event)
            self.scaling_key_down = True


    def on_key_up(self, event):
        if event.key == self.moving_key:
            if self.mouse_is_down and not self.scaling_key_down:
                self.transformer.stop_moving(event)
            elif self.mouse_is_down and self.scaling_key_down:
                self.transformer.start_scaling(event)
            self.moving_key_down = False
        elif event.key == self.scaling_key:
            if self.mouse_is_down and not self.moving_key_down:
                self.transformer.stop_scaling(event)
            elif self.mouse_is_down and self.moving_key_down:
                self.transformer.start_moving(event)
            self.scaling_key_down = False

    def on_mouse_down(self, event):
        if not (self.scaling_key_down and self.moving_key_down):
            if self.moving_key_down:
                self.transformer.start_moving(event)
            elif self.scaling_key_down:
                self.transformer.start_scaling(event)
        self.mouse_is_down = True

    def on_mouse_up(self, event):
        if not (self.scaling_key_down and self.moving_key_down):
            if self.moving_key_down:
                self.transformer.stop_moving(event)
            elif self.scaling_key_down:
                self.transformer.stop_scaling(event)
        self.mouse_is_down = False
