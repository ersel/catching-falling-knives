from flask import Flask
import json
import pandas
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from wsj_scraper import WSJSpider, get_previous_weekday
from twisted.internet import reactor
from scrapy import signals
from io import StringIO
app = Flask(__name__)

@app.route('/')
def index():
    # settings = Settings()
    # settings.set('USER_AGENT', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
    # settings.set('ITEM_PIPELINES', {'wsj_pipeline.StocksPipeline':1000})
    # process = Crawler(WSJSpider, settings)

    # # listen to spider_closed event and stop reactor
    # process.signals.connect(stop_reactor, signal=signals.spider_closed)
    # process.crawl(WSJSpider)

    # # reactor run blocks the process, until spider finishes
    # reactor.run()

    picks, csv = analyze_stocks()
    upload_csv(csv)

    # shorten the url
    # TODO: send sms with twilio

    return "Hello, world!", 200

def stop_reactor():
    reactor.callFromThread(reactor.stop)

def upload_csv(csv):
    import boto
    import boto.s3

    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    # https://docs.aws.amazon.com/general/latest/gr/rande.html
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, host='s3.eu-west-2.amazonaws.com')
    filename = '{}.csv'.format(get_previous_weekday())
    bucket = conn.get_bucket('daily-stock-data')
    key = boto.s3.key.Key(bucket, filename)
    key.set_contents_from_string(csv)
    key.set_acl('public-read')

def analyze_stocks():
    with open('decliners.json') as json_data:
        decliners_dict = json.load(json_data)
        df = pandas.DataFrame.from_dict(decliners_dict, orient='index')

        # pick companies which are cashflow positive and has paid a dividend last year
        cols = ['pe_ratio', 'dividend_yield']
        df[cols] = df[df[cols] > 0][cols]
        filtered = df.dropna()
        ranked = filtered.sort_values(by=['pe_ratio', 'dividend_yield', 'price_decline_percentage'], ascending=[True, False, True])

        buff = StringIO()
        ranked.to_csv(buff)
        buff.seek(0)
        csv = buff.getvalue()
        buff.close()

        return ranked.values.tolist(), csv

# We only need this for local development.
if __name__ == '__main__':
    app.run()
