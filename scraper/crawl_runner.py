# taken from https://stackoverflow.com/a/37270442/1124076
from scrapy import signals
from scrapy.crawler import CrawlerRunner

class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all stocks scraped
        self.symbols = {}

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        if len(item.keys()) == 4:
            # add symbol to dict
            self.symbols[item['symbol']] = item
        elif len(item.keys()) == 3:
            # merge ratio data
            symbol_data = self.symbols[item['symbol']]
            merged_data = {**symbol_data, **item}
            self.symbols[item['symbol']] = merged_data

    def return_items(self, result):
        return self.symbols
