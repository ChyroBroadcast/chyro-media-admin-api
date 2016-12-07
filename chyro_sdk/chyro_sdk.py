# Chyro SDK
# Should work with Python 2 & 3
#
# Copyright (C) 2016:
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
    def __init__(self, host, user, password, log=False):
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
        url = self._make_url('get', resource)
        url += '?' + urlencode(filters)
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

    def playlist(self, iso_day, bc, norm):
        url = self._make_url('export', 'daily', norm)
        url += '?begin={iso_day}&bc={bc}'.format(**locals())
        res = self.opener.open(url)
        return res.read()

    def set_rtb(self, media_id):
        url = self._make_url('tools', 'setrtb')
        url += '?id=' + media_id
        res = self.opener.open(url)
        return res.read()
        
def print_json(data):
    ''' pretty-printer '''
    print(json.dumps(data,
                     sort_keys=True,
                     indent=2,
                     separators=(',', ': ')))


