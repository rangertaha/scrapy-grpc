"""Scrapy extension that serves a gRPC control interface for the crawler.

:class:`WebService` reads the ``GRPC_ENABLED``, ``GRPC_HOST``, and
``GRPC_PORT`` settings and starts a :class:`grpc.Server` when the crawler
engine starts. :class:`CrawlerServicer` implements the RPCs defined in
``scrapy_grpc/pb/scrapy_grpc.proto``.
"""

from __future__ import annotations

import logging
from concurrent import futures
from typing import TYPE_CHECKING, Any

import grpc
from scrapy import Spider, signals
from scrapy.exceptions import NotConfigured

from scrapy_grpc.pb import scrapy_grpc_pb2, scrapy_grpc_pb2_grpc

if TYPE_CHECKING:
    from scrapy.crawler import Crawler

logger = logging.getLogger(__name__)

STOP_GRACE_SECONDS = 5.0


class CrawlerServicer(scrapy_grpc_pb2_grpc.CrawlerServicer):
    """Serve status, stats, and graceful shutdown for a Scrapy crawler."""

    def __init__(self, webservice: WebService) -> None:
        self._webservice = webservice

    def GetStatus(
        self,
        request: scrapy_grpc_pb2.StatusRequest,
        context: grpc.ServicerContext,
    ) -> scrapy_grpc_pb2.StatusResponse:
        crawler = self._webservice.crawler
        spider = getattr(crawler, "spider", None)
        return scrapy_grpc_pb2.StatusResponse(
            spider=spider.name if spider is not None else "",
            running=bool(crawler.crawling),
            items_scraped=self._webservice.items_scraped,
        )

    def GetStats(
        self,
        request: scrapy_grpc_pb2.StatsRequest,
        context: grpc.ServicerContext,
    ) -> scrapy_grpc_pb2.StatsResponse:
        stats = self._webservice.crawler.stats
        snapshot = stats.get_stats() if stats is not None else {}
        return scrapy_grpc_pb2.StatsResponse(
            stats={key: str(value) for key, value in snapshot.items()}
        )

    def StopCrawler(
        self,
        request: scrapy_grpc_pb2.StopRequest,
        context: grpc.ServicerContext,
    ) -> scrapy_grpc_pb2.StopResponse:
        crawler = self._webservice.crawler
        stopping = bool(crawler.crawling)
        if stopping:
            # RPCs run on gRPC worker threads; crawler shutdown must happen
            # on the Twisted reactor thread.
            from twisted.internet import reactor

            logger.info("Graceful shutdown requested over gRPC")
            reactor.callFromThread(crawler.stop)
        return scrapy_grpc_pb2.StopResponse(stopping=stopping)


class WebService:
    """Scrapy extension exposing the crawler over gRPC.

    Enable it via the ``EXTENSIONS`` setting and set ``GRPC_ENABLED`` to
    ``True``. The server listens on ``GRPC_HOST:GRPC_PORT`` (default
    ``127.0.0.1:6080``); a ``GRPC_PORT`` of ``0`` binds a free port, and
    :attr:`port` is updated to the bound port once the server starts.
    """

    def __init__(self, crawler: Crawler) -> None:
        if not crawler.settings.getbool("GRPC_ENABLED"):
            raise NotConfigured
        self.crawler = crawler

        self.port: int = crawler.settings.getint("GRPC_PORT", 6080)
        self.host: str = crawler.settings.get("GRPC_HOST", "127.0.0.1")
        self.items_scraped = 0
        self._server: grpc.Server | None = None

        crawler.signals.connect(self.start_listening, signals.engine_started)
        crawler.signals.connect(self.stop_listening, signals.engine_stopped)
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> WebService:
        return cls(crawler)

    def start_listening(self) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        scrapy_grpc_pb2_grpc.add_CrawlerServicer_to_server(
            CrawlerServicer(self), server
        )
        bound_port = server.add_insecure_port(f"{self.host}:{self.port}")
        if bound_port == 0:
            raise RuntimeError(f"Failed to bind gRPC server to {self.host}:{self.port}")
        server.start()
        self.port = bound_port
        self._server = server
        logger.info("gRPC service listening on %s:%d", self.host, self.port)

    def stop_listening(self) -> None:
        if self._server is not None:
            self._server.stop(grace=STOP_GRACE_SECONDS).wait()
            self._server = None
            logger.info("gRPC service stopped")

    def item_scraped(self, item: Any, spider: Spider) -> None:
        self.items_scraped += 1
        logger.debug(
            "Item scraped by spider %r (%d total)", spider.name, self.items_scraped
        )
