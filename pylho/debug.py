"""
"""
import time
import colors
import numpy as np
from collections import OrderedDict


class Logger(object):
    """ """
    def __init__(self, prefix, verbosity_level=1,
                 level_colors=['green', 'blue', 'purple', 'cyan']):
        self.prefix = prefix + ' '
        self.colors = level_colors
        self.verbosity_level = verbosity_level

    def __call__(self, text_str, verbose=0, color=None):
        # verbose: -1 => warning, verbose -2 => error
        # if no verbosity
        if (self.verbosity_level < verbose or verbose == 0) and verbose != -2:
            return
        # else print depending on level

        v = verbose - 1
        # get text color, depending if user specifies own color
        if color is None:
            color = self.colors[v]

        prefix = colors.color_text(self.prefix, color) + '... ' * v
        print("%s %s" % (prefix, text_str))


class Timer(object):
    """ """
    def __init__(self):
        self.timers = OrderedDict()

    def __call__(self, time_key):
        self.start(time_key)

    def start(self, time_key):
        self.timers[time_key] = time.time()

    def end(self, time_key):
        if time_key not in self.timers:
            ret = -1
        else:
            ret = time.time() - self.timers[time_key]
            self.timers[time_key] = ret
        return ret

    def summary(self):
        return ['%s: %0.3f secs' % (k, v) for k, v in self.timers.iteritems()]

    def print_summary(self):
        timers = self.summary()
        for s in timers:
            print(s)
