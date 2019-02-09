'''
Boxplot using bokeh
'''
import pandas as pd
import numpy as np
import os
import pandas as pd
import bokeh.io as bki
import bokeh.models as bkm
import bokeh.plotting as bkp
import bokeh.transform as bkt
import bokeh.layouts as bkl
from pylho import colors as pycolor
import copy
import bokeh


def find_unique_keep_order(seq):
    '''Finds unique values of a sequence, keeping order'''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def boxplot(df, x_cols, output_path,
            group_col=None, fig_kwargs=None,
            y_tick_fontsize='14pt', x_tick_fontsize='10pt',
            x_tick_orientation=np.pi/4.0, fa=0.85):
    '''Given long-format data, computes standard boxplot'''
    if fig_kwargs is None:
        fig_kwargs = {'height': 600, 'width': 1300, 'toolbar_location': 'above'}

    if group_col is None:
        df['_groups'] = '_'
        group_col = '_groups'

    # --- get data --- #
    colour_wheel = pycolor.colour_wheel(color_palette=pycolor.palettes.category20_alt)
    gb = df.groupby(group_col)
    groups = find_unique_keep_order(df[group_col])
    x_colors = {x: colour_wheel.next() for x in groups}
    ngroups = len(groups)
    x_width = 1 / float(ngroups + 1) - 0.02
    total_width = x_width * ngroups

    # initialize variables to store data
    invis_label_data = {'top': [], 'bottom': [], 'left': [], 'right': [], 'color': [], 'alpha': [], 'label': []}
    bw_b_data = {'top': [], 'bottom': [], 'left': [], 'right': [], 'color': [], 'alpha': [], 'variable': [], 'fimp_str': [], 'group': []}
    bw_m_data = {'xs': [], 'ys': [], 'color': [], 'alpha': []}
    bw_w_data =  {'xs': [], 'ys': [], 'color': [], 'alpha': []}
    bw_o_data = {'x': [], 'y': [], 'color': [], 'alpha': []}

    # loop through each x and get data
    for i_group, group in enumerate(groups):
        group_df = df.iloc[gb.indices[group]]

        # compute boxplot data
        q1s = group_df.quantile(q=0.25)
        q2s = group_df.quantile(q=0.50)
        q3s = group_df.quantile(q=0.75)
        iqrs = q3s - q1s
        uppers = q3s + 1.5 * iqrs
        lowers = q3s - 1.5 * iqrs
        vcolor = x_colors[group]

        # loop through each variable and add data
        x_offset = float(i_group) / float(ngroups + 1) - total_width / 2.0
        for i_col, col in enumerate(x_cols):
            q1 = q1s.loc[col]
            q1 = q1s.loc[col]
            q2 = q2s.loc[col]
            q3 = q3s.loc[col]
            upper = np.min([uppers.loc[col], group_df[col].max()])
            lower = np.max([lowers.loc[col], group_df[col].min()])

            # fill box data
            left = i_col + x_offset
            right = i_col + x_offset + x_width
            top = q3
            bottom = q1
            color = vcolor
            alpha = 0.15
            variable = col
            fimp_str = '%0.2f [%0.2f, %0.2f]' % (q2, q1, q3)

            bw_b_data['top'].append(top)
            bw_b_data['bottom'].append(bottom)
            bw_b_data['left'].append(left)
            bw_b_data['right'].append(right)
            bw_b_data['color'].append(color)
            bw_b_data['alpha'].append(alpha)
            bw_b_data['variable'].append(variable)
            bw_b_data['fimp_str'].append(fimp_str)
            bw_b_data['group'].append(group)

            # fill median data
            xs = [[i_col + x_offset, i_col + x_offset + x_width]]
            ys = [[q2, q2]]
            cs = [vcolor] * len(xs)
            aa = [1.0] * len(xs)

            bw_m_data['xs'].extend(xs)
            bw_m_data['ys'].extend(ys)
            bw_m_data['color'].extend(cs)
            bw_m_data['alpha'].extend(aa)

            # fill whisker data
            xs = [[i_col + x_offset, i_col + x_offset + x_width],
                  [i_col + x_offset, i_col + x_offset + x_width],
                  [i_col + x_offset + x_width/2.0, i_col + x_offset + x_width/2.0],
                  [i_col + x_offset + x_width/2.0, i_col + x_offset + x_width/2.0]]
            ys = [[upper, upper], [lower, lower], [lower, q1], [upper, q3]]
            cs = [vcolor] * len(xs)
            aa = [0.5] * len(xs)

            bw_w_data['xs'].extend(xs)
            bw_w_data['ys'].extend(ys)
            bw_w_data['color'].extend(cs)
            bw_w_data['alpha'].extend(aa)

            # fill outliers
            outliers = (group_df[col] > upper) | (group_df[col] < lower)
            y = list(group_df[col][outliers].values)
            x = [i_col + x_offset + x_width/2.0] * len(y)
            color = [vcolor] * len(y)
            alpha = [0.15] * len(y)

            bw_o_data['x'].extend(x)
            bw_o_data['y'].extend(y)
            bw_o_data['color'].extend(color)
            bw_o_data['alpha'].extend(alpha)

    # --- construct figure --- #
    bki.output_file(output_path)
    p = bkp.figure(**fig_kwargs)
    p.yaxis.major_label_text_font_size = y_tick_fontsize
    p.xaxis.major_label_text_font_size = x_tick_fontsize
    p.xaxis.axis_line_width = 2
    p.xgrid.grid_line_alpha = 0.0
    p.x_range.range_padding = 0.05
    p.y_range.range_padding = 0.05
    p.xaxis.major_label_orientation = x_tick_orientation

    # store legend items
    legend_items = []

    # hover
    hover = bkm.HoverTool(names=['box'], tooltips=[('variable', '@variable'), ('median [q1, q3]', '@fimp_str'), ('group', '@group')])
    p.add_tools(hover)

    # invisible line to label groups
    invis_label_src = bkm.ColumnDataSource(invis_label_data)
    r = p.quad(top='top', bottom='bottom', left='left', right='right', color='color', fill_alpha='alpha', source=invis_label_src, name='box', legend='label', muted_alpha=0)

    # box and whiskers objects
    # - box: [upper to lower]
    bw_b_data_src = bkm.ColumnDataSource(bw_b_data)
    r = p.quad(top='top', bottom='bottom', left='left', right='right', color='color', fill_alpha='alpha', source=bw_b_data_src, name='box', muted_alpha=0)
    legend_items.append(bkm.LegendItem(label='box', renderers=[r]))

    # - median
    bw_m_data_src = bkm.ColumnDataSource(bw_m_data)
    r = p.multi_line(xs='xs', ys='ys', color='color', alpha='alpha', source=bw_m_data_src, muted_alpha=0, line_width=2)
    legend_items.append(bkm.LegendItem(label='median', renderers=[r]))

    # - whiskers: [upper, lower]
    bw_w_data_src = bkm.ColumnDataSource(bw_w_data)
    r = p.multi_line(xs='xs', ys='ys', color='color', alpha='alpha', source=bw_w_data_src, muted_alpha=0)
    legend_items.append(bkm.LegendItem(label='whiskers', renderers=[r]))

    # - circle scatter: outliers
    bw_o_data_src = bkm.ColumnDataSource(bw_o_data)
    outlier_jitter = bkt.Jitter(width=x_width)
    r = p.circle(x={'field': 'x', 'transform': outlier_jitter}, y='y', color='color', alpha='alpha', source=bw_o_data_src, size=2, muted_alpha=0)
    legend_items.append(bkm.LegendItem(label='outliers', renderers=[r]))

    ## - plot 0 line
    #zero_line = bkm.Span(location=0, dimension='width', line_color='black', line_dash='solid', line_width=2)
    #p.add_layout(zero_line)

    # set data
    bw_b_data_src.data = bw_b_data
    bw_m_data_src.data = bw_m_data
    bw_w_data_src.data = bw_w_data
    bw_o_data_src.data = bw_o_data

    # fill invisible label data
    invis_data = copy.deepcopy(invis_label_data)
    for i_slice, pop_slice in enumerate(groups):
        invis_data['top'].append(0.1)
        invis_data['bottom'].append(0.1)
        invis_data['left'].append(0)
        invis_data['right'].append(0)
        invis_data['color'].append(x_colors[pop_slice])
        invis_data['alpha'].append(0.4)
        invis_data['label'].append('%s [%i encounters]' % (pop_slice, len(gb.indices[pop_slice])))
    invis_label_src.data = invis_data

    # legend
    legend = bkm.Legend(items=legend_items, location=(0, 0), click_policy='mute', background_fill_alpha=0.0, border_line_width=0.0)
    p.add_layout(legend, 'right')

    # set new p axis tick labels
    p.xaxis.ticker = np.arange(len(bw_b_data['variable']))
    p.xaxis.major_label_overrides = {i: x for i, x in enumerate(bw_b_data['variable'])}

    # save & return
    bki.save(p)
    return p
