==============
scrapy-grpc
==============

scrapy-grpc is an extension to control a running Scrapy web crawler via
gRPC. The service provides access to the main Crawler object.


Installation
============

Install scrapy-grpc using ``pip``::

    $ pip install scrapy-grpc


Configuration
=============

First, you need to include the entension to your ``EXTENSIONS`` dict in
``settings.py``, for example::

    EXTENSIONS = {
        'scrapy_grpc.webservice.WebService': 500,
    }

Then, you need to enable the extension with the `GRPC_ENABLED`_ setting,
set to ``True``.

The web server will listen on a port specified in `GRPC_PORT`_
(by default, it will try to listen on port 6080),
and will log to the file specified in `GRPC_LOGFILE`_.

The endpoint for accessing the crawler object is::

    http://localhost:6080/crawler


Example client
==============

A Python client is included::

    from scrapy_grpc import client
    ...

Settings
========

These are the settings that control the web service behaviour:

GRPC_ENABLED
---------------

Default: ``False``

A boolean which specifies if the web service will be enabled (provided its
extension is also enabled).

GRPC_LOGFILE
---------------

Default: ``None``

A file to use for logging HTTP requests made to the web service. If unset web
the log is sent to standard scrapy log.

GRPC_PORT
------------

Default: ``[6080, 7030]``

The port range to use for the web service. If set to ``None`` or ``0``, a
dynamically assigned port is used.

GRPC_HOST
------------

Default: ``'127.0.0.1'``

The interface the web service should listen on.

.. _gRPC: https://grpc.io
