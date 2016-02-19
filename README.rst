===============
Sift Python SDK
===============

A Python wrapper around `Sift API <http://sift.easilydo.com>`_. Currently
supports Python 2.7.11 and Python 3.5.1.

Installation
------------

**From the repository**

``python setup.py install``

**From pip**

``pip install siftapi``

Usage
-----
.. code-block:: python

  import siftapi

  sift = siftapi.Sift(API_KEY, API_SECRET)
  sift.get_user(<username>)

Testing
-------

``python setup.py test``

Test cases are written in ``tests`` folder.

**Files required for test cases:**

1. ``sensitive.py`` - File containing your API_SECRET and API_KEY. An example
   file, ``sensitive.py.example`` can be found in the directory
2. ``test.eml`` - A test ``.eml`` file to be sent for parsing

Documentation
-------------

Documentation for the SDK can be found `here <https://github.com/agent8/sift-python-sdk/blob/master/docs/API.rst>`__.

Changelog
---------

Changelog can be found `here <https://github.com/agent8/sift-python-sdk/blob/master/docs/CHANGELOG.rst>`__.
