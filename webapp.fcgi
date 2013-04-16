#!/usr/bin/python

#activate_this = '/var/www/at/wirwollendatenschutz/www/cgi-bin/venv/bin/activate_this.py'
import os
activate_this = os.getcwd() + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from flup.server.fcgi import WSGIServer
from webapp import app

if __name__ == '__main__':
	WSGIServer(app, bindAddress='/tmp/at.wirwollendatenschutz-fcgi.sock').run()
