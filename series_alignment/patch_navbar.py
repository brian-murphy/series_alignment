"""Implements a monkey patch for the matplotlib navigation bar backend.
This allows us to intercept events to navigation bar controls when we
are using the scaling tool.

Technique found at https://stackoverflow.com/a/15109266/1429640"""

from matplotlib.backend_bases import NavigationToolbar2

BASE_PRESS_PAN = NavigationToolbar2.press_pan
BASE_PRESS_ZOOM = NavigationToolbar2.press_zoom
BASE_RELEASE_PAN = NavigationToolbar2.release_pan
BASE_RELEASE_ZOOM = NavigationToolbar2.release_zoom
BASE_DRAG_PAN = NavigationToolbar2.drag_pan
BASE_DRAG_ZOOM = NavigationToolbar2.drag_zoom

class NavBarPatcher:
    """Monkey patch to make sure the Navigation Toolbar controls
    aren't activated when a target key is pressed. Must retain
    an instance of this so that the event listeners are not GCed"""
    def __init__(self, canvas, target_keys):
        self.canvas = canvas
        self.former_state = None
        self.target_keys = target_keys
        self.target_key_down = False

        self.canvas.mpl_connect('key_press_event', self.on_key_down)
        self.canvas.mpl_connect('key_release_event', self.on_key_up)

        NavigationToolbar2.press_pan = make_patch(self, BASE_PRESS_PAN)
        NavigationToolbar2.press_zoom = make_patch(self, BASE_PRESS_ZOOM)
        NavigationToolbar2.release_pan = make_patch(self, BASE_RELEASE_PAN)
        NavigationToolbar2.release_zoom = make_patch(self, BASE_RELEASE_ZOOM)
        NavigationToolbar2.drag_pan = make_patch(self, BASE_DRAG_PAN)
        NavigationToolbar2.drag_zoom = make_patch(self, BASE_DRAG_ZOOM)

    def on_key_down(self, event):
        if event.key in self.target_keys:
            self.target_key_down = True 

    def on_key_up(self, event):
        if event.key in self.target_keys:
            self.target_key_down = False

def make_patch(patcher, function):
    """wraps a function by only invoking it when the target key isn't down"""
    def wrapper_function(self, *args, **kwargs):
        if not patcher.target_key_down:
            function(self, *args, **kwargs)

    return wrapper_function
