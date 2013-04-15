from webapp import (app, cache)
import psycopg2
from json import dumps as jsondumps
from psycopg2.extras import RealDictCursor

from flask import (render_template, request, redirect, url_for, jsonify)
from flask.views import MethodView


URL_FORM = '/unterstuetzen'
URL_FORMACTION = '/unterstuetzerinnen'

TEMPLATE_FORM = 'unterstuetzen.html'
TEMPLATE_LIST_POST = 'thx.html'
TEMPLATE_EMAIL_DUPLICATE = 'email_duplicate.html'

FORM_CHECK_BLANK_FIELD = 'country'



@app.route(URL_FORMACTION)
def suporter_view():
    supporters = (list)(app.supporter_db.public_supporters())
    for i in supporters:
        i['firstname'] = i['firstname'].decode('utf8')
        i['lastname'] = i['lastname'].decode('utf8')
        i['town'] = i['town'].decode('utf8')
    return render_template(TEMPLATE_LIST_POST, supporters=supporters)

@app.route(URL_FORMACTION, methods=['POST'])
def add_suporter_view():
    # check if our spam textfield is filled in
    if (FORM_CHECK_BLANK_FIELD and request.form[FORM_CHECK_BLANK_FIELD] != ""):
        return redirect(url_for(TEMPLATE_FORM))
    
    # check referrer
    if not request.referrer.endswith(URL_FORM):
        return redirect(url_for(TEMPLATE_FORM))
    
    # full form data for json storage
    data = {'postdata': request.form}
    
    # mandatory fields
    for key in ['firstname', 'lastname', 'town', 'emailaddress' ]:
        if( (key not in request.form) or (request.form[key].strip()) == ''):
            return render_template(TEMPLATE_FORM, formdata=request.form, formerror=True)
        data[key] = request.form[key].strip()
    
    # email address
    if( (not '@' in request.form['emailaddress'])
        or (not '.' in request.form['emailaddress']) 
        or (len(request.form['emailaddress']) < 6)):
        del(data['emailaddress'])
        return render_template(TEMPLATE_FORM, formdata=data, formerror=True)
    
    # checkboxes
    for key in ['publicvisible', 'campaign_info']:
        if((key in request.form) and (request.form[key] == '1')):
            data[key] = True
        else:
            data[key] = False
    
    try:
        app.supporter_db.add(data)
    except psycopg2.IntegrityError:
        try:
            app.supporter_db.close()
        except:
            pass
        return render_template(TEMPLATE_EMAIL_DUPLICATE)
    
    supporters = (list)(app.supporter_db.public_supporters())
    for i in supporters:
        i['firstname'] = i['firstname'].decode('utf8')
        i['lastname'] = i['lastname'].decode('utf8')
        i['town'] = i['town'].decode('utf8')
     
    return render_template(TEMPLATE_LIST_POST, supporters=supporters, signed=True)





class SupporterDB():
    def __init__(self):
        self.conn = None
    
    def connect(self):
        self.conn = psycopg2.connect(**app.config['DATABASE_CONFIG'])
        
        
    @cache.memoize(120) # cache for  120 sec
    def count(self):
        if(self.conn == None):
            self.connect()
        cur = self.conn.cursor()
        cur.execute('SELECT count(*) FROM supporters;')
        count = cur.fetchone()[0]
        cur.close()
        return count
    
    def add(self, data):
        if(self.conn == None):
            self.connect()
        cur = self.conn.cursor()
        
        # no escaping needed, psycopg and jinja takes care of that.
        cur.execute(
        """INSERT INTO supporters (created, firstname, lastname, town, 
                emailaddress, publicvisible, campaign_info, post_data )
        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (data['firstname'], data['lastname'], data['town'], data['emailaddress'],
            data['publicvisible'], data['campaign_info'], jsondumps(data['postdata']) )
        )
        self.conn.commit()
        cur.close()
        # delete cached data
        cache.delete_memoized(self.count)
        cache.delete_memoized(self.public_supporters)
    
    @cache.memoize(120) # cache for  120 sec
    def public_supporters(self):
        if(self.conn == None):
            self.connect()
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
        """SELECT  id, firstname, lastname, town FROM supporters
            WHERE publicvisible=true
            ORDER BY id DESC
            LIMIT %d""" % app.config['SUPPORTER_COUNT'])
        resp = cur.fetchall()
        cur.close()
        return resp
    
    def close(self):
        if(self.conn != None):
            self.conn.close()
            self.conn = None
    def teardown(self, exception):
        self.close()

app.supporter_db = SupporterDB()
app.teardown_appcontext(app.supporter_db.teardown)

