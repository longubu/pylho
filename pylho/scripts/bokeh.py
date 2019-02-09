'''

'''
from bokeh.command.bootstrap import main
def run_server(python_path, port=5008, show=False):
    commands = ['bokeh', 'server', '--port %i' % port, '--allow-websocket-origin=10.252.98.245:%i' % port, python_path]
    main(commands)
