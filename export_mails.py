#!/usr/bin/env python

import os
activate_this = os.getcwd() + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import psycopg2
from psycopg2.extras import RealDictCursor
from optparse import OptionParser
from webapp.settings import DATABASE_CONFIG

def get_emails(options):

    # connect
    conn = psycopg2.connect(**DATABASE_CONFIG)

    # get new coursor
    # cur = conn.cursor(cursor_factory=RealDictCursor)
    cur = conn.cursor()

    if options.full:
        cur.execute(
        """SELECT  emailaddress FROM supporters
            ORDER BY id ASC"""  )
    else:
        filters = []
        if options.public:
            filters.append('publicvisible=true')
        if options.campaign:
            filters.append('campaign_info=true')

        cur.execute(
        """SELECT  emailaddress FROM supporters
            WHERE %s
            ORDER BY id ASC""" % ' AND '.join(filters) )

    resp = cur.fetchall()

    resp = map(lambda x: x[0], resp)

    print ',\n'.join(resp)

    conn.close()


parser = OptionParser()
parser.add_option("--public", action="store_true", dest="public", default=False)
parser.add_option("--campaign", action="store_true", dest="campaign", default=False)
parser.add_option("--full",     action="store_true", dest="full", default=False)
#parser.add_option("-h", "--help", action="help")

(options, args) = parser.parse_args()

if (options.full ^ (options.campaign or options.public)):
    get_emails(options)
else:
    parser.print_help()

