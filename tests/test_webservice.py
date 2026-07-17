import logging
from typing import Any

import pytest
from pydispatch import dispatcher
from scrapy import Spider, signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.test import get_crawler

from scrapy_grpc.webservice import WebService


def test_disabled_by_default() -> None:
    crawler = get_crawler()
    with pytest.raises(NotConfigured):
        WebService.from_crawler(crawler)


def test_enabled_with_defaults() -> None:
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)
    assert service.host == "127.0.0.1"
    assert service.port == 6080
    assert service.crawler is crawler


def test_custom_host_and_port() -> None:
    crawler = get_crawler(
        settings_dict={
            "GRPC_ENABLED": True,
            "GRPC_HOST": "0.0.0.0",
            "GRPC_PORT": 9090,
        }
    )
    service = WebService.from_crawler(crawler)
    assert service.host == "0.0.0.0"
    assert service.port == 9090


def test_start_listening_logs(caplog: pytest.LogCaptureFixture) -> None:
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)
    with caplog.at_level(logging.DEBUG, logger="scrapy_grpc.webservice"):
        service.start_listening()
    assert "Start listening" in caplog.text


def test_stop_listening_logs(caplog: pytest.LogCaptureFixture) -> None:
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)
    with caplog.at_level(logging.DEBUG, logger="scrapy_grpc.webservice"):
        service.stop_listening()
    assert "Stop listening" in caplog.text


def test_item_scraped_logs(caplog: pytest.LogCaptureFixture) -> None:
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)
    spider = Spider(name="dummy")
    with caplog.at_level(logging.INFO, logger="scrapy_grpc.webservice"):
        service.item_scraped({"title": "example"}, spider)
    assert "scraped" in caplog.text
    assert "example" in caplog.text


def test_signal_handlers_connected() -> None:
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)

    def receivers(signal: object) -> list[Any]:
        return list(
            dispatcher.liveReceivers(dispatcher.getAllReceivers(crawler, signal))
        )

    assert service.start_listening in receivers(signals.engine_started)
    assert service.stop_listening in receivers(signals.engine_stopped)
    assert service.item_scraped in receivers(signals.item_scraped)
