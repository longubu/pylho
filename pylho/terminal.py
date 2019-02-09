'''
Utility functions for dealing with terminal

pd.set_option('precision',4)

# multi-index slicing
df.loc[pd.IndexSlice[:, 12:], :]
  or
df.loc[(slice(None), slice(12, None)), :]
'''
import pandas as pd
import os
import numpy as np


def print_dict(d, filler='... '):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            print('%s%s' % (filler, k))
            print_dict(v, filler=(filler + filler))
        else:
            print('%s%s: %s' % (filler, k, v))


def import_runfile():
    import os
    os.environ['QT_API'] = 'pyqt'

    from spyder.utils.site.sitecustomize import runfile
    return runfile


def run_script(driver_path, description=None, args=None):
    '''
    Runs python script with logging information sent to vpicu-gpu slack channel
    Uses spyderlab's runfile to run python script; this is so we can maintain
    locals() variables after finishing script.

    # Argument
    driver_path: [str] Path to python file

    description: [str] Description associated with run to prefix logs. If
                 None, will use driver_path basename

    args: [str] Arguments to pass to driver_path
    '''
    from pylho import alerts
    runfile = import_runfile()
    import gc

    if description is None:
        description = os.path.basename(driver_path)

    if args is None:
        args = ''

    alerts.send_slack('[Starting] %s' % description)
    try:
        runfile(driver_path, args=args, wdir=os.path.dirname(driver_path))
        alerts.send_slack('[Done] %s' % description)
    except Exception as e:
        alerts.send_slack('[%s] Found error:\n%s' % (description, e))

    gc.collect()
    return locals()


def set_terminal(max_rows=40, precision=4, threshold=100, not_scientific=True):
    '''Resets terminal for neater printing of dataframes'''
    # set pandas stuff
    w, h = pd.io.formats.terminal.get_terminal_size()
    h = int(2.0/3.0 * h)
    pd.set_option('display.width', w)
#    pd.set_option('display.height', h)
    pd.set_option('max_rows', max_rows)
    pd.set_option('precision', precision)

    # set numpy stuff
    np.set_printoptions(precision=precision, threshold=threshold, linewidth=w, suppress=not_scientific)

    return '[Success] Set pandas terminal: [width %i] | [max_rows %i] | [precision %i]' % (w, max_rows, precision)


def print_dfs(dfs, names=None, stdout=True):
    '''
    Neatly prints to dataframes next to each other.

    # Arguments
    df1: [pd.DataFrame] df1
    df2: [pd.DataFrame] df2
    name1: [str] Name to title df1
    name2: [str] Nmae to title df2
    '''
    SPACER = '   |   '
    if not isinstance(dfs, list):
        raise RuntimeError('dfs needs to be a list of dataframes. got %s' % type(dfs))

    if names is not None:
        if not isinstance(names, list):
            raise RuntimeError('names need to be a list of strings. got %s' % type(names))

        if len(names) != len(dfs):
            raise RuntimeError('len(names) != len(dsfs). need to provdie same length names')
    else:
        names = ['df%i' % i for i in range(len(dfs))]

    # make sure dfs are dataframes and not series, series is a little different
    dfs_str = [pd.DataFrame(df).__str__().split('\n') for df in dfs]

    # find lowest dataframe length
    min_length = np.min([len(x) for x in dfs_str])

    # also index locates to min_length so all dataframes will print same length
    dfs_str = [df_str[:min_length] for df_str in dfs_str]

    # construct string list to print
    ret = [''.join(['%s' % n + ' ' * (len(df_str[0]) - len(n) + len(SPACER)) for df_str, n in zip(dfs_str, names)])]
    for i in range(min_length - 2):
        ret.append(''.join([df_str[i] + SPACER for df_str in dfs_str]))

    ret = '\n'.join(ret)
    if stdout:
        print(ret)

    return ret
