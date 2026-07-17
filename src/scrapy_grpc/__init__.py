"""Scrapy extension to control a running crawler via gRPC.

The implemented entry point is :class:`scrapy_grpc.webservice.WebService`,
a Scrapy extension that reads the ``GRPC_ENABLED``, ``GRPC_HOST``, and
``GRPC_PORT`` settings and hooks into the crawler lifecycle signals. The
gRPC service itself and the Python client are not implemented yet.
"""
