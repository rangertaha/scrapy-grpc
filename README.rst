===========
scrapy-grpc
===========

.. image:: https://img.shields.io/pypi/v/scrapy-grpc.svg
   :target: https://pypi.org/project/scrapy-grpc/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/scrapy-grpc.svg
   :target: https://pypi.org/project/scrapy-grpc/
   :alt: Supported Python versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/rangertaha/scrapy-grpc/blob/master/LICENSE.txt
   :alt: License

.. image:: https://github.com/rangertaha/scrapy-grpc/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/rangertaha/scrapy-grpc/actions/workflows/ci.yml
   :alt: CI status

scrapy-grpc is a Scrapy_ extension to control a running Scrapy web crawler
via gRPC_. It hooks into the crawler's lifecycle signals and exposes the
main ``Crawler`` object over a gRPC service.

.. note::
   This project is under active development. The extension currently wires
   up the crawler signals; the gRPC service interface and Python client are
   still being built out.


Installation
============

Install scrapy-grpc using ``pip``::

    $ pip install scrapy-grpc


Configuration
=============

First, include the extension in the ``EXTENSIONS`` dict in your project's
``settings.py``::

    EXTENSIONS = {
        "scrapy_grpc.webservice.WebService": 500,
    }

Then enable the extension by setting `GRPC_ENABLED`_ to ``True``.

The gRPC server will listen on the interface and port specified by
`GRPC_HOST`_ and `GRPC_PORT`_ (by default, ``127.0.0.1:6080``).


Settings
========

These are the settings that control the extension's behaviour:

GRPC_ENABLED
------------

Default: ``False``

A boolean which specifies if the gRPC service will be enabled (provided its
extension is also enabled).

GRPC_HOST
---------

Default: ``'127.0.0.1'``

The interface the gRPC service should listen on.

GRPC_PORT
---------

Default: ``6080``

The port to use for the gRPC service.


Development
===========

Clone the repository and install with the dev dependency group::

    $ git clone https://github.com/rangertaha/scrapy-grpc.git
    $ cd scrapy-grpc
    $ pip install -e . --group dev

Run the checks::

    $ ruff check src/ tests/
    $ mypy src/ tests/
    $ pytest --cov=scrapy_grpc


License
=======

MIT — see `LICENSE.txt`_.

.. _Scrapy: https://scrapy.org
.. _gRPC: https://grpc.io
.. _LICENSE.txt: https://github.com/rangertaha/scrapy-grpc/blob/master/LICENSE.txt
