from flask import render_template
from webapp import (app, cache)
from webapp.utils import add_template_rules

# import database functions and views
#import webapp.database

# add static templates
add_template_rules([
#   ['/url',            'templatefile.hmtl',    'optionalViewName'],
    ['/',               'index.html',       'index'],
    ['/kontakt',        'kontakt.html'],
    ['/positionen',     'positionen.html'],
    ['/unterstuetzen',  'unterstuetzen.html'],
    ['/presse',         'presse.html'],
    ['/impressum',      'impressum.html']
])

# custom error handlers
@app.errorhandler(405)
def err_405(e):
    return render_template('error-405.html'), 405

@app.errorhandler(404)
def err_404(e):
    return render_template('error-404.html'), 404

@app.errorhandler(403)
def err_403(e):
    return render_template('error-403.html'), 403