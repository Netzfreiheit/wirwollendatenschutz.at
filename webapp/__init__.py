from flask import Flask
from flask.ext.cache import Cache

try:
	import webapp.settings
except:
	import webapp.settings_sample as settings

# flask app
app = Flask(__name__)
app.config.from_object(settings)

# create cache instance
cache = Cache()

@app.before_first_request
def cacheinit():
    if app.debug:
        # no caching if in debug mode
        app.config['CACHE_TYPE'] = 'null'
    cache.init_app(app)

# import views
import webapp.views

