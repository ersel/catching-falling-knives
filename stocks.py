import json
from klein import Klein
import os
from lib.analyze_symbols import analyze_stocks
from lib.send_sms import text_daily_picks
from lib.shorten_url import shorten
from lib.upload_s3 import upload_csv
from lib.sample import get_sample
from scraper.crawl_runner import MyCrawlerRunner
from scraper.wsj_spider import WSJSpider

from twisted.internet import reactor
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

app = Klein()

@app.route("/")
def hello():
    return 'ok'

def schedule(request):
    runner = MyCrawlerRunner()
    spider = WSJSpider()
    dispatcher.connect(reactor.stop, signal=signals.spider_closed)
    defered = runner.crawl(spider)
    defered.addCallback(process_decliners)
    reactor.run()
    return "ok"

def process_decliners(decliners):
    picks, csv = analyze_stocks(decliners)
    long_url = upload_csv(csv)
    short_url = shorten(long_url)
    report = text_daily_picks(picks, short_url)
    return report

def load_env_vars():
    json_data = open('env_vars.json')
    env_vars = json.load(json_data)
    for key, val in env_vars.items():
        os.environ[key] = val

load_env_vars()
if __name__ == "__main__":
    app.run("localhost", 8080)
