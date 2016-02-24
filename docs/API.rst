===
API
===

This page contains information on the SDK's classes, methods and functions.

class Sift
==========

A client for EasilyDo's Sift API. Sift is an Artificial Intelligence for Email
that creates relevant features for your users with an email parse API that
simplifies and understands mail.

You can read more about `Sift here`_.

.. _Sift here: https://sift.easilydo.com

**Parameters**

* ``api_key`` - A ``string`` that can be found from the `developer's dashboard`_
* ``api_secret`` - A ``string`` that can be found from
  the `developer's dashboard`_

.. _developer's dashboard: https://sift.easilydo.com/sift/dashboard

**Example**

.. code-block:: python

    import siftapi

    sift = siftapi.Sift(api_key='<api_key here>', '<api_secret here>')

Methods
-------

discovery
^^^^^^^^^

Returns the parsed ``eml`` file as a ``dict``. ``eml`` files are *plain text in
MIME format*, containing the email header as well as the message econtents and
attachments.

**Parameters**

* ``filename``: A ``string`` that is the absolute path of the ``eml`` file.

**Example**

.. code-block:: python

    parsed_eml = sift.discovery('/path/to/file')
    print(parsed_eml)

add_user
^^^^^^^^

Adds a new user with the given username. The add connections API will
automatically create an account if it doesn't exist.

**Parameters**

* ``user``: A ``string`` that is the expected username of the new user.
* ``locale``: A ``string`` that is the locale of the new user.

**Example**

.. code-block:: python

    sift.add_user('username', 'en_US')

remove_user
^^^^^^^^^^^

Removes a user with the given username.

**Parameters**

* ``user``: A ``string`` that is the expected username of the user to be removed.

**Example**

.. code-block:: python

    sift.remove_user('username')

get_email_connections
^^^^^^^^^^^^^^^^^^^^^

Get all email connections linked to the user account.

**Parameters**

* ``user``: A ``string`` that is the expected username of the user to obtain
  the email connections from.

**Example**

.. code-block:: python

    sift.get_email_connections('username')

add_email_connection
^^^^^^^^^^^^^^^^^^^^

Adds a new email connection to the user account.

**Parameters**

* ``user``: A ``string`` that is the expected username of the user to add
  the email connection to.
* ``data``: Account specific parameters, see below for which parameter to include.

**Account Specific Parameters**

*Gmail*

.. code-block:: python

    {
      "account_type": "google",
      "account": <Email address associated with Google>,
      "refresh_token": <The refresh token for the OAuth2 connection>
    }

*Yahoo*

.. code-block:: python

    {
      "account_type": "yahoo",
      "account": <Email address associated with Yahoo>,
      "refresh_token": <The refresh token for the OAuth2 connection,>
      "redirect_uri": <The redirect URI that was used for the OAuth2 connection>
    }

*Microsoft Live/Hotmail*

.. code-block:: python

    {
      "account_type": "live",
      "refresh_token": <The refresh token for the OAuth2 connection>,
      "redirect_uri": <The redirect URI that was used for the OAuth2 connection>
    }

*IMAP*

.. code-block:: python

    {
      "account_type": "imap",
      "account": <Email address associated with the IMAP account>,
      "password": <Password for the IMAP account>,
      "host": <Host for the IMAP account>
    }

*Exchange*

.. code-block:: python

    {
      "account_type": "exchange",
      "email": <Email address for the Exchange account>,
      "password": <Password for the Exchange account>,
      "host": <Host of the exchange account> (Optional),
      "account": <Username for the Exchange account> (Optional)
    }

**Example**

.. code-block:: python

    # For a Gmail account
    params = {
      "account_type": "google",
      "account": "username@gmail.com",
      "refresh_token": "token"
    }
    sift.add_email_connection('username', params)

delete_email_connection
^^^^^^^^^^^^^^^^^^^^^^^

Deletes an email connection from the given user.

**Parameters**

* ``user``: A ``string`` that is the username of the user to be remove the
  connection from.
* ``connection_id``: A ``integer`` that is the connection_id of the email
  connection to be removed.

**Example**

.. code-block:: python

    sift.delete_email_connection('username')

get_sifts
^^^^^^^^^

Gets all Sifts(tasks) from the user.

**Parameters**

* ``user``: A ``string`` that is the username of the user to get the Sifts from.
* ``limit`` (Optional): An ``integer`` that is the maximum number of results to
    return.
* ``offset``: An ``integer``, starts the list at this offset (zero-based).
* ``last_update_time``: An ``integer`` which is an Epoch timestamp. Returns
    results with last update time more recent than this time.

**Example**

.. code-block:: python

    sift.get_sifts('username')

get_sift
^^^^^^^^^

Gets a single Sift(task) from the user.

**Parameters**

* ``user``: A ``string`` that is the username of the user to get the Sift from
* ``sift_id``: An ``integer`` that is the ID of the Sift to get from the user

**Example**

.. code-block:: python

    sift.get_sift('username', 123)

get_sift
^^^^^^^^^

Gets a single Sift(task) from the user.

**Parameters**

* ``user``: A ``string`` that is the username of the user to get the Sift from
* ``sift_id``: An ``integer`` that is the ID of the Sift to get from the user

**Example**

.. code-block:: python

    sift.get_sift('username', 123)

get_token
^^^^^^^^^

Get a new token for specific user.

**Parameters**

* ``user``: A ``string`` that is the username of the user to get the token for.

**Example**

.. code-block:: python

    sift.get_token('username')

post_feedback
^^^^^^^^^^^^^

Gives feedback to the EasilyDo team.

**Parameters**

* ``email``: A ``string`` that is the contents of the eml file, similar to the
  one sent to ``discovery``
* ``locale``: A ``string`` that is the locale of the email.
* ``timezone``: A ``string`` that is the timezone of the email

**Example**

.. code-block:: python

    data = open('/path/to/eml', r)
    sift.post_feedback(data, 'en_US', 'America/Los_Angeles')

