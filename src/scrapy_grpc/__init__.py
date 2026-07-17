"""Scrapy extension to control a running crawler via gRPC.

:class:`WebService` is a Scrapy extension that serves a gRPC control
interface (status, stats, graceful shutdown) for the running crawler, and
:class:`CrawlerClient` is the matching Python client. The service interface
is defined in ``scrapy_grpc/pb/scrapy_grpc.proto``.
"""

from scrapy_grpc.client import CrawlerClient
from scrapy_grpc.webservice import WebService

__all__ = ["CrawlerClient", "WebService"]
