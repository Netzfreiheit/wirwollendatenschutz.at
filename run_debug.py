#!/usr/bin/env python
#activate_this = '/var/www/at/wirwollendatenschutz/www/cgi-bin/venv/bin/activate_this.py'
import os
activate_this = os.getcwd() + '/venv/bin/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))

from webapp import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

