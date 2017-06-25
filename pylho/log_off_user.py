"""
Forcefully log off linux user from server
"""
import subprocess
import sys


class BashError(Exception):
    """Raises error if bash command was not successfully executed"""
    def __init__(self, cmd, err):
        self.msg = "Error executing bash command: %s"
        self.msg += '\n========== Err ============\n'
        self.msg += err

    def __str__(self):
        return repr(self.msg)


def find_user(user_num, tty=False):
    """Finds PID associated with login of user_num. if tty=True, will search
    for tty user (aka local)"""
    if tty:
        prefix = 'tty'
    else:
        prefix = 'pts/'

    cmd = 'ps -dN|grep %s%i' % (prefix, user_num)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()

    if err:
        raise BashError(cmd, err)

    return out.split(prefix)[0].strip()


def kill_pid(pid):
    """Kills -9 based on PID"""
    cmd = 'kill -9 %s' % pid
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()

    if err:
        raise BashError(cmd, err)


def log_off_user(user_num, tty=False):
    """Forcefully logs off user identified user_num (use `who`). if tty=True,
    will search for tty user (aka local)"""
    pid = find_user(user_num, tty=tty)
    kill_pid(pid)
    pid = find_user(user_num, tty=tty)
    if pid:
        raise Exception("Could not log off user: %s" % user_num)

    print("Successfully logged off %s" % user_num)


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 2:
        raise Exception("Too many system arguments",
                        "Only argument is user_num (int)")
    user_num = int(args[1])
    log_off_user(user_num)
