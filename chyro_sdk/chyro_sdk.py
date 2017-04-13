# Chyro SDK
# Should work with Python 2 & 3
#
# Copyright (C) 2017:
#       Chyro Conseil <support@chyro.tv>
#       License: MIT
#

import sys
import os
import urllib
import json

# Python 2
if sys.version_info[0] == 2:
    import urllib2, cookielib
    from urllib import urlencode
# Python 3
else:
    import functools
    import urllib.request as urllib2
    from urllib.parse import urlencode
    import http.cookiejar as cookielib

class Error(Exception):
    pass

class Chyro(object):
    def __init__(self, host, user, password, bc=1, log=False):
        self.log = log
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        auth_data = urlencode({'user': user, 'password': password})
        try:
            res = opener.open('http://{host}/api/auth/gettoken/format/json'.format(host=host) + '?' + auth_data)
        except urllib2.URLError as e:
            raise Error(e)
        data = json.loads(res.read().decode('ascii'))
        if self.log: print(data)
        token = data['token']
        if not token:
            raise Error('Invalid credentials')
        self.opener = opener
        self.token = token
        self.host = host
        self.cj = cj
        self.bc = bc

    def _make_url(self, module, resource, form='json'):
        host = self.host
        url = 'http://{host}/api/{module}/{resource}/format/{form}'.format(**locals())
        return url

    def search(self, resource, **filters):
        query = ''.join('{%s==%s}' % (k, v) for k,v in filters.items())
        url = self._make_url('search', resource)
        url += '?' + urlencode({'query': query})
        opener = self.opener
        if self.log: print('GET ' + url)
        res = opener.open(url)
        return json.loads(res.read().decode('utf-8'))['data']

    def get(self, resource, **filters):
        bc = str(self.bc)
        url = self._make_url('get', resource)
        url += '?' + urlencode(filters)
        url += '&broadcast=' + bc
        opener = self.opener
        if self.log: print('GET ' + url)
        res = opener.open(url)
        return json.loads(res.read().decode('utf-8'))[resource]

    def update(self, target, id, data):
        url = self._make_url('set', 'quickupdate')
        qs = urlencode({
            'target': target,
            'reference_ids': json.dumps({target+'_id': id}),
            'perform': True,
            'fields': json.dumps(data),
        })
        res = self.opener.open(url + '?' + qs)
        return res.read()

    def playlist(self, iso_date, norm):
        bc = self.bc
        url = self._make_url('export', 'daily', norm)
        url += '?begin={iso_date}&bc={bc}'.format(**locals())
        res = self.opener.open(url)
        return res.read()

    def set_rtb(self, media_id):
        url = self._make_url('tools', 'setrtb')
        url += '?id=' + media_id
        res = self.opener.open(url)
        return res.read()

    def triggerbypost(self, pgm_id, media_name, file_location):
        print('triggerbypost')
        post_params = urlencode({
            'program_program_id': pgm_id,
            'media_part': 1,
            'media_endpart': 1,
            'media_filelocation': file_location,
            'mediaagentrepository_id': 16,
            'media_filename': media_name, # Name in  IMPORT
            'media_name': media_name,     # Name in Chyro DB
            'media_version': 32,
            'mediatype_mediatype_id': 9,
            'physicalmedia_physicalmedia_id': 'all',
            'workflowType': 'importMedia',
            'targetType': 'program',
            'targetQuery': ('{id==%s}' % pgm_id),
        })
        url = self._make_url('workflow', 'triggerbypost')
        res = self.opener.open(url, data=post_params) # This is a POST
        print(res)
        print(post_params)
        return True

    def send_email(self, template, *params):
        email_params = ','.join(str(p) for p in params)
        url = self._make_url('mail', 'send')
        qs = urlencode({
            'template': template,
            'params': email_params,
        })
        url += '?' + qs
        print(url)
        res = self.opener.open(url).read()
        return res

def print_json(data):
    ''' pretty-printer '''
    print(json.dumps(data,
                     sort_keys=True,
                     indent=2,
                     separators=(',', ': ')))
