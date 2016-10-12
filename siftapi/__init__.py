#!/usr/bin/env python
# coding=utf8

import json
import hashlib
import hmac
import time
import requests

from . import version
from . import utils
from . import exceptions

build_url = utils.build_url
VERSION = version.__version__


class Sift:
    def __init__(self, api_key, api_secret, env='production'):
        self._env = env
        self.api_key = api_key
        self.api_secret = api_secret

    def _request(self, method, url, params=None, data=None):
        args = {}
        if params is None:
            params = {}
        if data is None:
            data = {}
        params.update(self._generate_required_params())
        args.update(params)
        args.update(data)

        params['signature'] = signature = self._generate_signature(
                args,
                method,
                '/%s%s' % (VERSION, url)
            ).hexdigest()
        url = build_url(self._env, url)

        try:
            r = requests.request(method, url, params=params, data=data)
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise APIError(response)
        except requests.Timeout:
            raise APIError({message: 'Request timeout.'})
            return

        return r.json()

    def _generate_signature(self, params, method, path):
        """Generates a signature based on the Sift documentation

        Params:
            `params`: Other params besides the common params
            `method`: GET/POST/PUT/DELETE
            `path`: Path of API endpoint
        """
        base_string = method + '&' + path
        for k in sorted(params):
            base_string += '&' + k + '=' + str(params[k])

        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.sha1
        )
        return signature

    def _generate_required_params(self):
        """Generates the required params of most Sift API requests"""
        return {
            'api_key': self.api_key,
            'timestamp': int(time.time())
        }

    def discovery(self, filename):
        """Discovery engine

        Params:
            `filename`: Absolute path of the .eml email file
        """
        with open(filename, 'r') as eml:
            eml = eml.read().strip()

        return self._request('POST', '/discovery', data={'email': eml})

    def add_user(self, user, locale):
        """Adds a new user

        Params:
            `user`: Username of the new user
            `locale`: Locale of the new user, e.g. en_US
        """
        data = {
            'username': user,
            'locale': locale,
        }
        return self._request('POST', '/users', data=data)

    def remove_user(self, user):
        """Removes a user

        Params:
            `user`: Username of the user to delete
        """
        return self._request('DELETE', '/users/%s' % user)

    def get_email_connections(self, user):
        """Get all email connections linked to the account

        Params:
            `user`: Username of the user
        """
        return self._request('GET', '/users/%s/email_connections' % user)

    def add_email_connection(self, user, data):
        """Link a new email connection to the account

        Params:
            `user`: Username of user to add email connection to

            `params`:

                # Gmail:
                {
                    "account_type": "google",
                    "account": <Email address associated with Google>,
                    "refresh_token": <The refresh token for the OAuth2
                                     connection>
                }

                # Yahoo:
                {
                    "account_type": "yahoo",
                    "account": <The Yahoo GUID associated with the user’s
                                      Yahoo account>,
                    "refresh_token": <The refresh token for the OAuth2
                                      connection>,
                    "redirect_uri": <The redirect URI that was used for
                                     the OAuth2 connection>
                }

                # Microsoft Live/Hotmail
                {
                    "account_type": "live",
                    "account": <Email address associated with the Live/Hotmail
                                     account>,
                    "refresh_token": <The refresh token for the OAuth2
                                     connection>,
                    "redirect_uri": <The redirect URI that was used for the
                                     OAuth2 connection>
                }

                # IMAP
                {
                    "account_type": "imap",
                    "account": <Email address for the IMAP account>,
                    "password": <Password for the IMAP account>,
                    "host": <Host for the IMAP account>
                }

                # Exchange
                {
                    "account_type": "exchange",
                    "email": <Email for the Exchange account>,
                    "password": <Password for the Excahnge account>,
                    "host": <Host of exchange account> (Optional),
                    "account": <Username for the Exchange account> (Optional)
                }
        """
        if data is None:
            raise APIError({message: 'Additional params are required'})
        return self._request(
                'POST',
                '/users/%s/email_connections' % user,
                data=data)

    def delete_email_connection(self, user, connection_id):
        """Deletes an email connection to the account

        Params:
            `user`: Username of user to delete email connection from
            `connection_id`: ID of connection to delete
        """
        return self._request(
                'DELETE',
                '/users/%s/email_connections/%s' % (user, connection_id)
            )

    def get_sifts(self, user, limit=100, offset=0, domains=None, last_update_time=0):
        """Get all Sifts from the user

        Params:
            `user`: Username of user to get Sifts from
        """
        params = {
            'limit': limit,
            'offset': offset,
            'last_update_time': last_update_time,
        }
        if domains:
            params['domains'] = ','.join(domains)
        return self._request('GET', '/users/%s/sifts' % user, params=params)

    def get_sift(self, user, sift_id, include_eml=0):
        """Get a single sift from the user

        Params:
            `user`: Username of user to get Sift from
            `sift_id`: ID of particular Sift to get
        """
        params = {
            'include_eml': include_eml
        }
        return self._request(
                'GET',
                '/users/%s/sifts/%s' % (user, sift_id)
            )

    def get_token(self, user):
        """Get a new token for specific user

        Params:
            `user`: Username of user to get token from
        """
        return self._request('POST', '/connect_token', data={'username': user})

    def post_feedback(self, email, locale, timezone):
        """Give feedback to the EasilyDo team

        Params:
            `email`: Contents of the eml file, similar to the one sent to
                     discovery API
            `locale`: Locale of the email, e.g. en_US
            `timezone`: Timezone of the email, e.g. America/Los_Angeles
        """
        data = {
            'email': email,
            'locale': locale,
            'timezone': timezone
        }
        return self._request('POST', '/feedback', data=data)
