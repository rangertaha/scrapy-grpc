"""Blocking Python client for the scrapy-grpc control service."""

from __future__ import annotations

from types import TracebackType

import grpc

from scrapy_grpc.pb import scrapy_grpc_pb2, scrapy_grpc_pb2_grpc


class CrawlerClient:
    """Client for the ``scrapy_grpc.Crawler`` gRPC service.

    Connects to the address served by the
    :class:`~scrapy_grpc.webservice.WebService` extension. Usable as a
    context manager::

        with CrawlerClient(port=6080) as client:
            print(client.status().items_scraped)
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 6080) -> None:
        self._channel = grpc.insecure_channel(f"{host}:{port}")
        self._stub = scrapy_grpc_pb2_grpc.CrawlerStub(self._channel)

    def status(self) -> scrapy_grpc_pb2.StatusResponse:
        """Return the spider name, running state, and items-scraped count."""
        return self._stub.GetStatus(scrapy_grpc_pb2.StatusRequest())

    def stats(self) -> dict[str, str]:
        """Return a snapshot of the crawler stats, values as strings."""
        response = self._stub.GetStats(scrapy_grpc_pb2.StatsRequest())
        return dict(response.stats)

    def stop_crawler(self) -> bool:
        """Request a graceful crawler shutdown; True if one was initiated."""
        response = self._stub.StopCrawler(scrapy_grpc_pb2.StopRequest())
        return bool(response.stopping)

    def close(self) -> None:
        self._channel.close()

    def __enter__(self) -> CrawlerClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
