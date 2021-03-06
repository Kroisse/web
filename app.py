"""GUI launcher for OS X

You can build it using py2app_::

   $ pip install py2app
   $ python setup.py build_sass
   $ python setup.py py2app

.. _py2app: https://pypi.python.org/pypi/py2app/

"""
import Tkinter as tk
import os.path
import threading
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse
import webbrowser

from earthreader.web.app import app, spawn_worker
from libearth.session import Session
from waitress.server import create_server


def serve():
    server.run()


def open_webbrowser(port):
    webbrowser.open('http://0.0.0.0:{}'.format(port))


if __name__ == "__main__":
    root = tk.Tk()
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label="Open Browser",
                         command=lambda: open_webbrowser(port))
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    root.withdraw()
    directory = os.path.expanduser('~/.earthreader')
    repository = urlparse.urljoin('file://', directory)
    session_id = Session().identifier
    app.config.update(REPOSITORY=repository, SESSION_ID=session_id)
    server = create_server(app, port=0)
    port = server.effective_port
    spawn_worker()
    proc = threading.Thread(target=serve)
    proc.daemon = True
    proc.start()
    open_webbrowser(port)
    root.mainloop()
