import pytest
from scrapy.exceptions import NotConfigured
from scrapy.utils.test import get_crawler

from scrapy_grpc.webservice import WebService


def test_disabled_by_default():
    crawler = get_crawler()
    with pytest.raises(NotConfigured):
        WebService.from_crawler(crawler)


def test_enabled_with_defaults():
    crawler = get_crawler(settings_dict={"GRPC_ENABLED": True})
    service = WebService.from_crawler(crawler)
    assert service.host == "127.0.0.1"
    assert service.port == 6080
    assert service.crawler is crawler


def test_custom_host_and_port():
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
