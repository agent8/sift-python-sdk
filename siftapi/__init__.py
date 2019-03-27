#!/usr/bin/env python
# coding=utf8

import json
import hashlib
import hmac
import time
import requests

from . import version
from .utils import build_url
from .exceptions import APIError

VERSION = version.__version__


class EmailFilterRuleException(Exception):
    """Raised when an email filter field is not a list."""
    pass


class Sift(object):
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

        params['signature'] = self._generate_signature(
            args,
            method,
            '/%s%s' % (VERSION, url)
        ).hexdigest()
        url = build_url(self._env, url)

        try:
            r = requests.request(method, url, params=params, data=data)
        except requests.HTTPError as e:
            raise APIError({'message': 'HTTPError raised.'})
        except requests.Timeout:
            raise APIError({'message': 'Request timeout.'})

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

    def _parse_filter_params(self, params):
        res = {}
        for field, filters in params.items():
            if not isinstance(filters, list):
                msg = '%s is not a list, not added as a filter param.' % field
                raise EmailFilterRuleException(msg)

            res[field] = json.dumps(filters)

        return res

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

    def get_email_connections(self, user, limit=100, offset=0, include_invalid=False):
        """Get all email connections linked to the account

        Params:
            `user`: Username of the user
        """
        params = {
            'limit': limit,
            'offset': offset,
            'include_invalid': 1 if include_invalid else 0
        }
        return self._request('GET', '/users/%s/email_connections' % user,
                             params=params)

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
            raise APIError({'message': 'Additional params are required'})
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
        params = {'include_eml': include_eml}
        return self._request('GET',
                             '/users/%s/sifts/%s' % (user, sift_id),
                             params=params)

    def get_token(self, user):
        """Get a new token for specific user

        Params:
            `user`: Username of user to get token from
        """
        return self._request('POST', '/connect_token', data={'username': user})

    def get_email(self, username, email_id):
        """Returns the email content using the information sent as a webhook to
        the developer.

        Params:
            `username`: Username of user to retrieve email for
            `email_id`: Unique ID of the email to retrieve the email for
        """
        path = '/users/%s/emails/%s' % (username, email_id)
        return self._request('GET', path)

    def get_emails_by_user(self, username, limit=100, offset=0):
        """Returns all emails for a specific user, this does not return the
        email content itself, only the metadata.

        Params:
            `username`: Username of user to get emails
            `limit`: The maximum number of results to return, defaults to 100
            `offset`: Start the list at this offset (0-indexed), defaults to 0
        """
        path = '/users/%s/emails' % username
        params = {'limit': limit, 'offset': offset}

        return self._request('GET', path, params=params)

    def get_emails_by_developer(self, limit=100, offset=0):
        """Returns all emails for the developer, this does not return the
        email content itself, only the metadata.

        Params:
            `limit`: The maximum number of results to return, defaults to 100
            `offset`: Start the list at this offset (0-indexed), defaults to 0
        """
        path = '/emails'
        params = {'limit': limit, 'offset': offset}

        return self._request('GET', path, params=params)

    def add_email_filter(self, description=None, **kwargs):
        """Creates a new email filter to get a webhook for.

        Params:
            `description`: Description of the filter
            `**kwargs`: Supported filter rules, each rule should be a list of
                filter strings as documented in the documentation.
        """
        path = '/emails/filters'
        data = self._parse_filter_params(kwargs)
        if description:
            data['description'] = description

        return self._request('POST', path, data=data)

    def get_email_filters(self, limit=100, offset=0):
        """Returns a list of email filters created by the developer.

        Params:
            `limit`: The maximum number of results to return, defaults to 100
            `offset`: Start the list at this offset (0-indexed), defaults to 0
        """
        path = '/emails/filters'
        params = {'limit': limit, 'offset': offset}

        return self._request('GET', path, params=params)

    def get_email_filter(self, filter_id):
        """Return the detail of a single email filter created by the developer.

        Params:
            `filter_id`: Unique ID of the filter
        """
        path = '/emails/filters/%s' % filter_id
        return self._request('GET', path)

    def delete_email_filter(self, filter_id):
        """Deletes the email filter created by the developer.

        Params:
            `filter_id`: Unique ID of the filter
        """
        path = '/emails/filters/%s' % filter_id
        return self._request('DELETE', path)

    def update_email_filter(self, filter_id, description=None, **kwargs):
        """Updates an existing email filter.

        Params:
            `filter_id`: Unique ID of the filter
            `...kwargs`: Fields as defined in the documentation page
        """
        path = '/emails/filters/%s' % filter_id
        data = self._parse_filter_params(kwargs)
        if description:
            data['description'] = description

        return self._request('PUT', path, data=data)

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
