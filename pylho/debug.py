"""
"""
import time
import colors


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


class Timer(Logger):
    """ """
    def __init__(self, *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)

    def start(self):
        self.start_time = time.time()

    def end(self):
        return time.time() - self.start_time
