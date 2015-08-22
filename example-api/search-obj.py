#!/usr/bin/python
# -*- coding: utf-8 -*-
#
##       Chyro API Model
##       <support@chyro.tv>
##      Install Python Modules
##              - urllib / urllib2
##              - cookielib
##              - simplejson
import urllib, urllib2, cookielib
import simplejson,os,sys


##
##      Setup
##

host="HOST" # Host, like preprod.mycompany.chyro.fr (without http://)
username="LOGIN" # Login with API read/write
password="PASS" # Password


##
##      Main code
##
class ChyroApi:
	def __init__(self, host, login, passwd, form = 'json'):
		self.host = host
		self.login = login
		self.passwd = passwd
		self.form = form
	
	def initAuth(self):
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		login_data = urllib.urlencode({'user' : self.login, 'password' : self.passwd})
		try:
			login = self.opener.open('http://%s/api/auth/gettoken/format/json' % self.host, login_data)
		except urllib2.URLError, e:
			return False
		try:
			login_response = simplejson.load(login)
		except ValueError:
			return False
		return login_response['token']

	def searchApi(self, sheet, token, query):
		try:
			resp = self.opener.open('http://%s/api/search/%s/format/%s?query=%s&token=%s' % (self.host, sheet, self.form, query, token))
		except urllib2.URLError, e:
			return False
		try:
			response = simplejson.load(resp)
		except ValueError:
			return False
		return response


if __name__ == "__main__":
	chyro = ChyroApi(host, username, password)
	token = chyro.initAuth()
	if token:
		print chyro.searchApi('program', token, '{title=test}')




		

