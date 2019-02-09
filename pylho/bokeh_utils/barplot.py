'''
Wrapper for plotting bar plots in bokeh easily and conveniently.

- This won't try to be as general and abstract as bokeh. We will assume
a common datastructure that we're used to -- pandas, along with
all of it's parent packages: numpy, etc.

What kind of generality am I trying to give it?

- plot multple bars for comparison next to each other, if user specifies additional column for "grouping"
- create a color categorical map also.



# Notes
- modified to not overwrite color when group is specified
'''
import pandas as pd
import numpy as np
import os
import pandas as pd
import bokeh.io as bki
import bokeh.models as bkm
import bokeh.plotting as bkp
import bokeh.transform as bkt
from pylho import colors as pycolor


def _plot_bar(p, x, y, x_map, x_offset=0, width=0.9, error=None, c=None, quad_kwargs=None, error_lw_kwargs=None, legend=None, group_name=None):
    '''boloblaw. not going to be documented. internal use only'''
    # argument checks
    if quad_kwargs is None:
        quad_kwargs = {}

    if error_lw_kwargs is None:
        error_lw_kwargs = {}

    # automatically get color if not specified
    if c is None:
        colour_wheel = pycolor.colour_wheel(pycolor.palettes.category20_alt)
        c = []
        for i in range(len(x)):
            c.append(colour_wheel.next())

    # get categorical name per x
    x_cat = [x_map[_x] for _x in x]

    # fix data up for bokeh quads
    left = np.array(x) - x_offset - width
    right = np.array(x) - x_offset + width
    top = [_y if _y >= 0 else 0 for _y in y]
    bottom = [_y if _y < 0 else 0 for _y in y]
    src = bkm.ColumnDataSource(data={'left': left, 'right': right, 'top': top, 'bottom': bottom, 'c': c, 'x_cat': x_cat, 'y': y, 'group': [group_name] * len(left)})

    # plot vertical bars
    p.quad(left='left', right='right', top='top', bottom='bottom', source=src, fill_color='c', legend=legend, line_alpha=0.0, **quad_kwargs)

    # plot error bars
    if error is not None:
        if len(error) != len(x):
            raise RuntimeError('Error vector needs to be equal length')

        xs = [[_x - x_offset, _x - x_offset] for _x in x]
        ys = [[_y - _e, _y + _e] for _y, _e in zip(y, error)]
        err_src = bkm.ColumnDataSource(data={'xs': xs, 'ys': ys, 'y': y, 'x_cat': x_cat})
        p.multi_line(xs='xs', ys='ys', source=err_src, **error_lw_kwargs)


def find_unique_keep_order(seq):
    '''Finds unique values of a sequence, keeping order'''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



def barplot(df, x_col, y_col, output_path,
            group_col=None, error_col=None, color_col=None,
            fig_kwargs=None, y_tick_fontsize='14pt', x_tick_fontsize='16pt',
            x_tick_orientation=np.pi/2.0, fa=0.85, err_lw=2):
    '''Plots vertical bar plots using bokeh. Strictly uses pd.DataFrame

    # Assumptions
    - user can put data in correct format. note: this is not at "smart" as seaborn
    - x is categorical
    - data isnt too big. not efficiently coded for large data

    # Arguments
    df: pd.DataFrame

    x_col: name of column in df to use as x-axis. assumes categorical

    y_col: name of column in df to use as y-axis. bar plot values.

    output_path: path to output html file

    group_col: name of column to groupby df to plot nested groupings

    error_col: col to use for plotting error bars. plots error symmetrically, aka  y +/- error

    color_col: col to use for coloring bars. if group_col is specified, color is chosen to override this column.

    fig_kwargs: dictionary argument to send to p.figure(). height, width, title etc

    y_tick_fontsize: this is a string with 'pt' attached

    x_tick_fontsize: this is a string with 'pt' attached

    x_tick_orientation: float. 0 for horizontal, np.pi/2.0 for vertical

    fa: fill_alpha of the bars. Globally applied to all bars

    err_lw: line width of the error bars. Globally applied to all bars
    '''
    if fig_kwargs is None:
        fig_kwargs = {'height': 600, 'width': 1300}

    # TODO: reevaluate me.
    # make a copy of df as to not edit the original data
    df = df.copy()

    # --- construct figure --- #
    bki.output_file(output_path)
    p = bkp.figure(**fig_kwargs)
    p.yaxis.major_label_text_font_size = y_tick_fontsize
    p.xaxis.major_label_text_font_size = x_tick_fontsize
    p.xaxis.axis_line_width = 2
    p.xgrid.grid_line_alpha = 0.0
    p.x_range.range_padding = 0.15
    p.y_range.range_padding = 0.1
    p.xaxis.major_label_orientation = x_tick_orientation
    quad_kwargs = {'line_color': None, 'line_width': 1, 'fill_alpha': fa}
    error_lw_kwargs = {'line_width': err_lw, 'color':'black'}

    # hover
    hover = bkm.HoverTool(tooltips=[('x', '@x_cat'), ('y', '@y'), ('group', '@group')])
    p.add_tools(hover)

    # find unique values of x and coordinate mapping to the categorical
    unique_xs = find_unique_keep_order(df[x_col])
#    x_plot = len(unique_xs)
    x_map = {i: x_name for i, x_name in enumerate(unique_xs)}
    p.xaxis.ticker = bkm.FixedTicker(ticks=range(len(x_map)))
    p.xaxis.formatter = bkm.FuncTickFormatter(code='''var labels = %s; return labels[tick];''' % x_map)

    if group_col is None:
        df['_groups'] = '_'
        group_col = '_groups'

    if color_col is None:
        color_col = '_color'
        df[color_col] = 'black'

        # if group is given, give a color
        if group_col != '_groups':
            colour_wheel = pycolor.colour_wheel(color_palette=pycolor.palettes.category20_alt)
            for k, indices in df.groupby(group_col).indices.iteritems():
                df[color_col].iloc[indices]  = next(colour_wheel)
        else:
            df[color_col] = 'black'

    gb = df.groupby(group_col)
    ngroups = gb.ngroups

    if ngroups > 1:
        x_offsets, x_width = np.linspace(0, 1.0, num=ngroups + 1, endpoint=False, retstep=True)
        x_offsets = (x_offsets - x_width)[:ngroups]
    else:
        x_offsets = [0]
        x_width = 0.9

    for i, (group_name, sub_df) in enumerate(gb):
        sub_df = sub_df.set_index(x_col)
        x_offset = x_offsets[i]
        y = list(sub_df.loc[unique_xs, y_col].fillna(value=0).values)
        x = range(len(y))

        if error_col is None:
            error = None
        else:
            error = sub_df[error_col].values

        if color_col is None:
            c = None
        else:
            c = sub_df[color_col].values

        if group_col == '_groups':
            leg = None
        else:
            leg = group_name

        _plot_bar(p, x, y, x_map, x_offset=x_offset, width=x_width/2.0, error=error, c=c,
                  quad_kwargs=quad_kwargs, error_lw_kwargs=error_lw_kwargs, legend=leg, group_name=group_name)

    p.x_range.start = x_offsets[0] - x_width
    p.x_range.end = len(x_map) - 1 + x_offsets[-1] + x_width
    p.legend.click_policy = 'hide'
    bki.save(p)
    return p


if __name__ == '__main__':
#    a = len(['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Straberries', 'x', '5', '6', '10', '11', '12', '13'])
#    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries', 'x', '5', '6', '10', '11', '12', '13'] * 3
#    counts = [5, 3, 4, 2, 4, 6, 1, 2, 3, 4, 5, 6, 7] + [5, 3, 4, 2, 4, 6, 1, 2, 3, 4, 5, 6, 7][::-1] + [5, 3, 4, 2, 4, 6, 1, 2, 3, 4, 5, 6, 7]
#    err_list = [0.1, 0.2, 0.3, 0.4, 0.5,  1, 2, 3, 4, 5, 6, 7, 0.3, 0.2, 0.3] + [0.1, 0.2, 0.3, 0.4, 0.5,  1, 2, 3, 4, 5, 6, 7, 0.3, 0.2, 0.3]  + [0.1, 0.2, 0.3, 0.4, 0.5,  1, 2, 3, 4, 5, 6, 7, 0.3, 0.2, 0.3][::-1]
#    gb_data = ['group1'] * a + ['group2'] * a + ['group3'] * a
#    colorz = ['black'] * len(gb_data)
#    df = pd.DataFrame(zip(fruits, counts, err_list, gb_data, colorz), columns=['fruits', 'counts', 'error', 'groups', 'colors'])

    # make test data
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries', 'x', '5', '6', '10', '11', '12', '13']
    counts = [5, 3, 4, 2, 4, 6, 1, 2, 3, 4, 5, 6, 7]
    err_list = [0.1, 0.2, 0.3, 0.4, 0.5,  1, 2, 3, 4, 5, 6, 7]
    gb_data = ['group1'] * len(fruits)
    colorz = ['black'] * len(gb_data)
    df = pd.DataFrame(zip(fruits, counts, err_list, gb_data, colorz), columns=['fruits', 'counts', 'error', 'groups', 'colors'])

    output_path = './test.html'
    x_col = 'fruits'
    y_col = 'counts'
    group_col = None # 'groups'
    error_col = 'error'  # None
    color_col = None  # 'colors'
    y_tick_fontsize = '5pt'  # '14pt'
    x_tick_fontsize = '10pt'  # '16pt'
    x_tick_orientation = np.pi / 2.0
    fig_kwargs = {'height': 400, 'width': 1500}
    fa = 0.8
    err_lw = 2

    p = barplot(df, x_col, y_col, output_path,
                group_col=group_col, error_col=error_col, color_col=color_col,
                fig_kwargs=fig_kwargs, y_tick_fontsize=y_tick_fontsize, x_tick_fontsize=x_tick_fontsize,
                x_tick_orientation = x_tick_orientation, fa=fa, err_lw=err_lw)
