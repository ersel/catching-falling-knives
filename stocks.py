from flask import Flask
import json
import pandas
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from wsj_scraper import WSJSpider
from twisted.internet import reactor
from scrapy import signals
app = Flask(__name__)

@app.route('/')
def index():
    settings = Settings()
    settings.set('USER_AGENT', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
    settings.set('ITEM_PIPELINES', {'wsj_pipeline.StocksPipeline':1000})
    process = Crawler(WSJSpider, settings)

    # listen to spider_closed event and stop reactor
    process.signals.connect(stop_reactor, signal=signals.spider_closed)
    process.crawl(WSJSpider)

    # reactor run blocks the process, until spider finishes
    reactor.run()

    analyze_stocks()

    # TODO: send sms with twilio

    return "Hello, world!", 200

def stop_reactor():
    reactor.callFromThread(reactor.stop)

def analyze_stocks():
    with open('decliners.json') as json_data:
        decliners_dict = json.load(json_data)
        decliners = pandas.DataFrame.from_dict(decliners_dict, orient='index')
        print(decliners)
        # TODO: weed out companies with negative p/e and no dividend record in the last year
        # TODO: sort remaining companies by biggest decline percentage, lowest p/e and highest dividend


# We only need this for local development.
if __name__ == '__main__':
    app.run()
