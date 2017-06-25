'''
Functions for selecting color.

# Notes
- Everything will operate in HEX by default, but there are functions to
    convert to RGB if needed.

# Theory of coloring data visualizations:
http://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf
- use color only to serve a particular communication goal
- use different colors only when they correspond to differences of meaning
    in the data (don't use it just for visual appeal. it distracts
    the user from making DIRECT comparisons. comparison graphs => single color)
    - What purpose will the color serve?
    - Will it serve this purpose effectively?
- use soft, natural colors to display most information and bright and/or dark
    colors to highlight information that requires greater attention
- for small data points/thin lines: use bright/dark colors.
- for thicker data points and thicker lines: use a medium shade palette
- use light/pale colors for parts of tables and graphs that don't display data (axes, text)
- When using color to encode a sequential range of quantitative values,
    stick with a single hue (or a small set of closely related hues) and vary
    intensity from pale colors for low values to increasingly darker and brighter
    colors for high values.

- Bars: Use a distinct hue of medium intensity for each data series.
- Lines: For thin lines, use a distinct hue of fairly high intensity for each; otherwise,
    use distinct hues of medium intensity.
- Data Points: For small points, use a distinct hue of fairly high intensity for each;
    otherwise, use distinct hues of medium intensity

# Resources
- http://colorbrewer2.org/
- http://www.colourlovers.com/palettes/most-favorites/all-time/meta
'''
import numpy as np


class palettes:
    '''list of carefully chosen palettes. view them using `colors.view_palette`
    '''
    # qualitative
    light = ['#FBB4AE', '#B3CDE3', '#CCEBC5', '#DECBE4', '#FED9A6', '#FFFFCC', '#E5D8BD', '#FDDAEC']
    light_dark = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#FB9A99', '#E31A1C', '#FDBF6F', '#FF7F00']
    medium = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5']
    dark = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF']

    medium_12 = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F']
    dark_12 = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#FB9A99', '#E31A1C', '#FDBF6F', '#FF7F00', '#CAB2D6', '#6A3D9A', '#FFFF99', '#B15928']

    # sequential
    hot = ['#FFFFCC', '#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026']
    cold = ['#F7FCF0', '#E0F3DB', '#CCEBC5', '#A8DDB5', '#7BCCC4', '#4EB3D3', '#2B8CBE', '#08589E']

    # diverging
    hot_cold = ['#D73027', '#F46D43', '#FDAE61', '#FEE090', '#E0F3F8', '#ABD9E9', '#74ADD1', '#4575B4']

    # set default
    default = medium

    # colourlover ones
    giant_goldfish = ['#69D2E7', '#A7DBD8', '#E0E4CC', '#F38630', '#FA6900', '#69D2E7', '#A7DBD8', '#E0E4CC']
    emo_kid =  ['#556270', '#4ECDC4', '#C7F464', '#FF6B6B', '#C44D58', '#556270', '#4ECDC4', '#C7F464']
    ring_toss = ['#94DBDF', '#8485B5', '#FC8EAB', '#DABEB2', '#FCF6D4', '#94DBDF', '#8485B5', '#FC8EAB']


def view_palette(color_palette, a=1.0):
    '''views a color palette (list of hex).

    # Arguments
    color_palette: [list] list of hex strings of each color

    a: [float] [Optional] Alpha amount to apply
    '''
    import matplotlib.pyplot as plt

    color_palette = _check_get_palette(color_palette)
    n = len(color_palette)

    plt.figure()
    plt.clf()
    plt.scatter(range(n), [1] * n, marker='s', s=500, c=color_palette, alpha=a)
    plt.xlim(-1, n)
    plt.ylim(0.5, 1.5)
    plt.xticks([])
    plt.yticks([])
    plt.grid(alpha=0.25)
    fig = plt.gcf()
    plt.show()
    return fig


class ascii:
    '''List of ascii prefix to apply coloring to strings in bash/terminal'''
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    GREY = '\033[0m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    DEFAULT = GREY


def color_string(string, color):
    '''Returns string modified with ascii coloring for printing in terminal.

    # Arguments
    string: [str] string to color

    # Returns
    string: modified string with ascii coloring.
    '''
    if not hasattr(ascii, color.upper()):
        raise RuntimeError('Do not recognize color: %s' % color)

    return '%s%s%s' % (getattr(ascii, color.uper()), string, ascii.DEFAULT)


def print_color(string, color):
    '''Prints string in certain color. See `colors.ascii` for list of colors'''
    print(color_string(string, color))


def _check_get_palette(color_palette):
    if color_palette is None:
        color_palette = palettes.default
    elif isinstance(color_palette, list):
        pass
    else:
        color_palette = getattr(palettes, color_palette)

    return color_palette


def random(n=1, color_palette=None):
    '''Randomly select n colors from a chosen color_palette
    (from colors.palette bank).

    # Arguments
    n: [int] Number of colors to choose from palette

    color_palette: [str] Name of color palette in colors.palette to use.
        If list or array-like, will assume a color palette list is
        already passed in and will randomly select from that list.

    # Return
    ret: [list] list of colors in HEX
    '''
    color_palette = _check_get_palette(color_palette)
    if len(color_palette) < n:
        raise RuntimeError('Not enough colors in palette (%s with %i colors) to choose %i.' % (color_palette, len(color_palette), n))

    idxs = np.random.choice(np.arange(len(color_palette)), size=n, replace=False)
    return list(np.array(color_palette)[idxs])


def color_array(arr, color_palette=None):
    '''
    Returns array containig color for each unique element in arr.

    # Example:
    arr = [1, 1, 0, 0]
    return = ['blue', 'blue', 'green', 'green']

    # Arguments
    arr: ndarray, iterable
        List of labels or distinguishing elements to assign colors to

    color_palette: [str] Name of color palette in colors.palette to use.
        If list or array-like, will assume a color palette list is
        already passed in and will randomly select from that list.

    # Returns
    color_arr: ndarray of HEX colors
        Returns an array where each element corresponds to a color within
        `arr`, mapped by unique elements of arr.
    '''
    color_palette = _check_get_palette(color_palette)
    uniques = np.unique(arr)
    n = len(uniques)
    if len(color_palette) < n:
        raise RuntimeError('Not enough colors in palette (%s with %i colors) to choose %i.' % (color_palette, len(color_palette), n))

    rng_colors = random(n=n, color_palette=color_palette)
    colors = dict(zip(uniques, rng_colors))
    color_arr = np.array([colors[x] for x in arr])
    return color_arr


def hex_to_rgb(value):
    '''Converts hex string to RGB tuple of length 3. If list or arr of
    hex strings, will convert each element to its RGB equivalent.'''
    if hasattr(value, '__len__') and (not isinstance(value, str)):
        ret = [hex_to_rgb(x) for x in value]
    else:
        value = value.lstrip('#')
        lv = len(value)
        ret = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return ret


def rgb_to_hex(rgb):
    '''Converts iterable rgb array to hex string. Can also be an iterable
    containing rgb arrays, in which this will return a list of hex strings'''
    rgb = np.array(rgb)
    shape = rgb.shape
    # if tuple/iterable of len(3) -- aka single RGB
    if shape == (3L,):
        ret = '#%02x%02x%02x' % tuple(rgb)
    # else if rgb is a batch of rgbs, recursively use rgb_to_hex
    elif shape[1] == 3:
        ret = np.array([rgb_to_hex(x) for x in rgb])
    else:
        raise RuntimeError("Do not understand %s to convert to hex" % rgb)

    return ret
