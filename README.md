
# About

This is a minimalistic python app to serve semi-static pages based on [flask][], a WSGI web microframework.

* [Jinja2][Jinja] templates
* [Flask-Cache][] for template caching
* [psycopg2][] (at the moment) as database backend

`database.py` provides a minimalistic PostgreSQL database backend to store form values, (the default form POST names are `firstname`, `lastname`, `town`, `publicvisible (bool)`, `campaign_info (bool)` and `emailaddress`)
Additionally all POST values are also seperately stored in JSON format to allow aditional form elements without changing the database structure.

# Installing
### python virtualenv setup
We are using a virtual python envoronment to not be forced to install flask globally.

To create a new virtual environment run the following in the root (this) directory:
```
virtualenv venv
. ./venv/bin/activate
```

### flask modules
```
pip install flask Flask-Cache
```

### database backend

For the database backend you will need also need the `psycopg2` package and its dependencies (or `python-psycopg2` on debian systems).
```
pip install psycopg2
```

# Settings
### basic settings

For the basic app settings create a `settings.py` file (just copy `settings_sample.py`).
Make sure to set `SECRET_KEY` to a random secret key, for example (taken from the flask docs):

```python
>>> import os
>>> os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
```

### database

To enable the database backend:

* set a valid `DATABASE_CONFIG` in `settings.py`
* edit `database.py` to your URLs / template files
* import `schema.sql` to your database and
* uncomment `import webapp.database` in `views.py`.

### cache setup

Template functions and data can automatically be cached by [Flask-Cache][], just set `CACHE_TYPE` in settings.py (and install its requirements).

# Development

`run_debug.py` starts Flask's powerful [development server][Flask-debug] on 0.0.0.0:8080.

**Warning:** The debug server should never be publically accessible, as it allows arbitrary code execution.

# Deployment

See [Flask's Deployment Options][Flask-deploy].

### FastCGI example

**Warning:** This is just an example, FastCGI is a real PITA to debug. You most likely don't want to use this. Also, if you change any Python files, you have to restart the CGI server.

`webapp.fcgi` is a FastCGI wrapper for the flask application, which provides a unix socket for the webserver. Most webservers don't start/monitor FastCGI processes automatically, so it has to be run seperately, we used [Supervisor][], but a simple start script / watchdog might also do the job.

##### nginx example config:

```
server {
    listen   80;
    listen   [::]:80 default ipv6only=on;

    server_name  wirwollendatenschutz.at;

    location / { try_files $uri @webapp; }
    location @webapp {
        include fastcgi_params;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param SCRIPT_NAME "";
        fastcgi_pass unix:/tmp/at.wirwollendatenschutz-fcgi.sock;
    }

    # serve static files directly
    location /static {
            root   /var/www/at/wirwollendatenschutz/www/cgi-bin/webapp;
    }
    location /favicon.ico {
        root   /var/www/at/wirwollendatenschutz/www/cgi-bin/webapp/static;
    }
    location /robots.txt {
        root   /var/www/at/wirwollendatenschutz/www/cgi-bin/webapp/static;
    }
}
```

# LICENSES & COPYRIGHT

unless otherwise stated:

**source code:** (basically all .py files) New BSD License (see `LICENSE_sourcecode`)
**Texts, artwork, etc...:** CC BY 3.0 (see `LICENSE_artwork_texts`)

# TODO

* use SQLAlchemy ORM instead of psycopg2 to support different database backends
* more flexible database backend
* more documentation


[flask]: http://flask.pocoo.org/
[Jinja]: http://jinja.pocoo.org/
[Flask-Cache]: http://pythonhosted.org/Flask-Cache/
[psycopg2]: http://initd.org/psycopg/docs/
[Flask-debug]: http://flask.pocoo.org/docs/quickstart/#debug-mode
[Flask-deploy]: http://flask.pocoo.org/docs/deploying/
[Supervisor]: http://supervisord.org/
