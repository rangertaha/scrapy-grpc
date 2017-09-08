import logging

from scrapy.exceptions import NotConfigured
from scrapy import signals
from scrapy.utils.reactor import listen_tcp


logger = logging.getLogger(__name__)


class WebService(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('GRPC_ENABLED'):
            raise NotConfigured
        self.crawler = crawler

        self.port = crawler.settings.get('GRPC_PORT', 6080)
        self.host = crawler.settings.get('GRPC_HOST', '127.0.0.1')

        crawler.signals.connect(self.start_listening, signals.engine_started)
        crawler.signals.connect(self.stop_listening, signals.engine_stopped)
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start_listening(self):
        logger.debug('Stat listening')

    def stop_listening(self):
        logger.debug('Stop listening')

    def item_scraped(self, item, spider):
        logger.info("scraped %s items", item)
