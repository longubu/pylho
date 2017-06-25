'''
Utility functions for dealing with terminal
'''
import pandas as pd
import os


def run_script(driver_path, description=None, args=None, verbose=True):
    '''
    Runs python script with logging information sent to vpicu-gpu slack chanenl

    # Argument
    driver_path: [str] Path to python file

    description: [str] Description associated with run to prefix logs. If
                 None, will use driver_path basename

    args: [str] Arguments to pass to driver_path

    verbose: [bool] Whether or not to prints stdout and stderr or script to
             local terminal
    '''
    from pylho import alerts
    from subprocess import Popen, PIPE
    if description is None:
        description = os.path.basename(driver_path)

    alerts.send_slack('[Starting] %s' % description)

    if isinstance(args, str):
        args = args.split(' ')
    elif isinstance(args, list):
        pass
    else:
        args = []

    try:
        proc = Popen(["/usr/local/anaconda/bin/python", driver_path] + args,
                     stdout=PIPE, stderr=PIPE)
        while True:
            retcode = proc.poll()
            if retcode is not None:
                if verbose:
                    print
                    print("----- STDOUT -----")
                    print(''.join(proc.stdout.readlines()))
                    print("----- STDERR -----")
                    print(''.join(proc.stderr.readlines()))
                    print
                break
        alerts.send_slack('[Done] %s' % description)
    except Exception as e:
        alerts.send_slack('Err %s. Found error:\n%s' % (driver_path, e))


def set_pandas_terminal(verbose=0):
    '''Resets terminal for neater printing of dataframes'''
    w, h = pd.util.terminal.get_terminal_size()
    h = int(2.0/3.0 * h)
    pd.set_option('display.width', w)
    pd.set_option('display.height', h)

    if verbose:
        print("Set terminal size to: (%i, %i)" % (w, h))


# build fancy print function to print x & y dataframes side by side.
def print_dfs(df1, df2, name1='df1', name2='df2'):
    '''
    Neatly prints to dataframes next to each other.

    # Arguments
    df1: [pd.DataFrame] df1
    df2: [pd.DataFrame] df2
    name1: [str] Name to title df1
    name2: [str] Nmae to title df2
    '''
    pd.set_option("display.max_rows", 20)
    df1_str = df1.__str__().split('\n')
    df2_str = df2.__str__().split('\n')
    ret = ["%s" % name1 + ' ' * len(df1_str[0]) + "%s" % name2]
    for i in range(len(df1_str) - 2):
        ret.append(df1_str[i] + '   |   ' + df2_str[i])
    print('\n'.join(ret))

