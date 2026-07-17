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
via gRPC_. It starts a gRPC server alongside the crawler engine and exposes
a ``Crawler`` service with three RPCs:

- ``GetStatus`` — the running spider's name, whether the engine is
  running, and the number of items scraped so far.
- ``GetStats`` — a snapshot of the crawler's stats collector.
- ``StopCrawler`` — request a graceful crawler shutdown.

The service interface is defined in
``src/scrapy_grpc/pb/scrapy_grpc.proto``, and a matching blocking Python
client, ``scrapy_grpc.CrawlerClient``, is included.


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


Usage
=====

With the extension enabled, control the running crawler from any process
using ``CrawlerClient``::

    from scrapy_grpc import CrawlerClient

    with CrawlerClient(host="127.0.0.1", port=6080) as client:
        status = client.status()
        print(status.spider, status.running, status.items_scraped)

        print(client.stats())     # dict[str, str] snapshot of crawler stats

        client.stop_crawler()     # graceful shutdown, like a single Ctrl-C

Any gRPC client in any language can talk to the service; generate stubs
from ``src/scrapy_grpc/pb/scrapy_grpc.proto``.


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

The port to use for the gRPC service. Set it to ``0`` to bind a free
ephemeral port.


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

After changing ``scrapy_grpc.proto``, regenerate the gRPC stubs::

    $ python -m grpc_tools.protoc -I src \
          --python_out=src --grpc_python_out=src \
          src/scrapy_grpc/pb/scrapy_grpc.proto


License
=======

MIT — see `LICENSE.txt`_.

.. _Scrapy: https://scrapy.org
.. _gRPC: https://grpc.io
.. _LICENSE.txt: https://github.com/rangertaha/scrapy-grpc/blob/master/LICENSE.txt
