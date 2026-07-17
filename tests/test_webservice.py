import logging
from typing import Any

import pytest
from pydispatch import dispatcher
from scrapy import Spider, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.utils.test import get_crawler

from scrapy_grpc import CrawlerClient, WebService


def enabled_crawler(**settings: Any) -> Crawler:
    return get_crawler(settings_dict={"GRPC_ENABLED": True, **settings})


def test_disabled_by_default() -> None:
    crawler = get_crawler()
    with pytest.raises(NotConfigured):
        WebService.from_crawler(crawler)


def test_enabled_with_defaults() -> None:
    crawler = enabled_crawler()
    service = WebService.from_crawler(crawler)
    assert service.host == "127.0.0.1"
    assert service.port == 6080
    assert service.crawler is crawler
    assert service.items_scraped == 0


def test_custom_host_and_port() -> None:
    crawler = enabled_crawler(GRPC_HOST="0.0.0.0", GRPC_PORT=9090)
    service = WebService.from_crawler(crawler)
    assert service.host == "0.0.0.0"
    assert service.port == 9090


def test_port_setting_accepts_strings() -> None:
    crawler = enabled_crawler(GRPC_PORT="9090")
    service = WebService.from_crawler(crawler)
    assert service.port == 9090


def test_item_scraped_counts_and_logs(caplog: pytest.LogCaptureFixture) -> None:
    service = WebService.from_crawler(enabled_crawler())
    spider = Spider(name="dummy")
    with caplog.at_level(logging.DEBUG, logger="scrapy_grpc.webservice"):
        service.item_scraped({"title": "example"}, spider)
        service.item_scraped({"title": "example"}, spider)
    assert service.items_scraped == 2
    assert "dummy" in caplog.text


def test_signal_handlers_connected() -> None:
    crawler = enabled_crawler()
    service = WebService.from_crawler(crawler)

    def receivers(signal: object) -> list[Any]:
        return list(
            dispatcher.liveReceivers(dispatcher.getAllReceivers(crawler, signal))
        )

    assert service.start_listening in receivers(signals.engine_started)
    assert service.stop_listening in receivers(signals.engine_stopped)
    assert service.item_scraped in receivers(signals.item_scraped)


def test_grpc_round_trip() -> None:
    service = WebService.from_crawler(enabled_crawler(GRPC_PORT=0))
    service.start_listening()
    assert service.port != 0
    try:
        with CrawlerClient(port=service.port) as client:
            status = client.status()
            assert status.running is False
            assert status.spider == ""
            assert status.items_scraped == 0

            service.item_scraped({"title": "example"}, Spider(name="dummy"))
            assert client.status().items_scraped == 1

            stats = client.stats()
            assert isinstance(stats, dict)

            # The crawler is not running, so no shutdown is initiated.
            assert client.stop_crawler() is False
    finally:
        service.stop_listening()


def test_stop_listening_without_start_is_noop() -> None:
    service = WebService.from_crawler(enabled_crawler())
    service.stop_listening()
