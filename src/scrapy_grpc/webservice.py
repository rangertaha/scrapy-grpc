from __future__ import annotations

import logging
from typing import Any

from scrapy import Spider, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class WebService:
    def __init__(self, crawler: Crawler) -> None:
        if not crawler.settings.getbool("GRPC_ENABLED"):
            raise NotConfigured
        self.crawler = crawler

        self.port = crawler.settings.get("GRPC_PORT", 6080)
        self.host = crawler.settings.get("GRPC_HOST", "127.0.0.1")

        crawler.signals.connect(self.start_listening, signals.engine_started)
        crawler.signals.connect(self.stop_listening, signals.engine_stopped)
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> WebService:
        return cls(crawler)

    def start_listening(self) -> None:
        logger.debug("Start listening")

    def stop_listening(self) -> None:
        logger.debug("Stop listening")

    def item_scraped(self, item: Any, spider: Spider) -> None:
        logger.info("scraped %s items", item)
