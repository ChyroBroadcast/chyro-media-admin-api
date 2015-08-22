#!/usr/bin/python
# -*- coding: utf-8 -*-
#
##       Chyro API Model
##       <support@chyro.fr>
##	Install Python Modules
##		- urllib / urllib2
##		- cookielib
##		- simplejson
import urllib, urllib2, cookielib
import simplejson,os,sys


##
##	Setup
##

host="HOST" # Host, like preprod.mycompany.chyro.fr (without http://)
username="LOGIN" # Login with API read/write
password="PASS" # Password



##
##	Main code
##
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'user' : username, 'password' : password})
try:
        login = opener.open('http://%s/api/auth/gettoken/format/json' % host, login_data)
except urllib2.URLError, e:
        print "CHYRO ERROR: Can't find host to login..."
        sys.exit(2)
try:
        login_response = simplejson.load(login)
except ValueError:
        print "CHYRO ERROR: no JSON item for login;"
        sys.exit(2)
if login_response['token'] == False:
        print "CHYRO ERROR: Can't login to Chyro Media Admin;"
        sys.exit(2)
else:
        # MY REQUEST
        try:
                resp = opener.open('http://%s/api/search/program/format/json?query={title=test}&token=%s' % (host, login_response['token']))
        except urllib2.URLError, e:
                if type(e) == urllib2.HTTPError:
                        print "CHYRO ERROR: Can't find Program Pages (%s);" % e.code
                else:
                        print "CHYRO ERROR: Can't find host...;"
                sys.exit(2)
        try:
                response = simplejson.load(resp)
        except ValueError:
                print "CHYRO ERROR: no JSON item;"
                sys.exit(2)

        print response
