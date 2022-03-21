#!/usr/bin/env python
# vim: set ts=4 sw=4 expandtab sts=4:
# Copyright (c) 2011-2013 Christian Geier & contributors
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Source: https://github.com/ljanyst/carddav-util/blob/master/carddav.py

#-------------------------------------------------------------------------------
# Lukasz Janyst:
#
# requests-0.8.2:
# * Remove the verify ssl flag - caused exception
# * Add own raise_for_status for more meaningful error messages
# * Fix digest auth
#-------------------------------------------------------------------------------

"""
contains the class PyCardDAV and some associated functions and definitions
"""

from collections import namedtuple
import requests
import urllib.parse as urlparse
import logging


def raise_for_status(resp):
    if 400 <= resp.status_code < 500 or 500 <= resp.status_code < 600:
        msg = 'Error code: ' + str(resp.status_code) + '\n'
        msg += str(resp.content)
        raise requests.exceptions.HTTPError(msg)


class PyCardDAV(object):
    """class for interacting with a CardDAV server
    Since PyCardDAV relies heavily on Requests [1] its SSL verification is also
    shared by PyCardDAV [2]. For now, only the *verify* keyword is exposed
    through PyCardDAV.
    [1] http://docs.python-requests.org/
    [2] http://docs.python-requests.org/en/latest/user/advanced/
    raises:
        requests.exceptions.SSLError
        requests.exceptions.ConnectionError
        more requests.exceptions depending on the actual error
        Exception (shame on me)
    """

    def __init__(self, resource, debug='', user='', passwd='',
                 verify=True, write_support=False, auth='basic'):
        #shutup url3
        urllog = logging.getLogger('requests.packages.urllib3.connectionpool')
        urllog.setLevel(logging.CRITICAL)

        split_url = urlparse.urlparse(resource)
        url_tuple = namedtuple('url', 'resource base path')
        self.url = url_tuple(resource,
                             split_url.scheme + '://' + split_url.netloc,
                             split_url.path)
        self.debug = debug
        self.session = requests.session()
        self.write_support = write_support
        self._settings = {'verify': verify}
        if auth == 'basic':
            self._settings['auth'] = (user, passwd,)
        if auth == 'digest':
            from requests.auth import HTTPDigestAuth
            self._settings['auth'] = HTTPDigestAuth(user, passwd)
        self._default_headers = {"User-Agent": "pyCardDAV"}
        response = self.session.request('PROPFIND', resource,
                                        headers=self.headers,
                                        **self._settings)
        raise_for_status(response)  # raises error on not 2XX HTTP status code

    @property
    def headers(self):
        return dict(self._default_headers)

    def get_vcard(self, href):
        """
        pulls vcard from server
        :returns: vcard
        :rtype: string
        """
        response = self.session.get(self.url.base + href,
                                    headers=self.headers,
                                    **self._settings)
        raise_for_status(response)
        return response.content
