import json
from klein import route, run
import os
from lib.analyze_symbols import analyze_stocks
from lib.sample import get_sample_data
from lib.send_sms import text_daily_picks
from lib.shorten_url import shorten
from lib.upload_s3 import upload_csv
from scraper.crawl_runner import MyCrawlerRunner
from scraper.wsj_spider import WSJSpider

@route("/")
def schedule(request):
    runner = MyCrawlerRunner()
    spider = WSJSpider()
    deferred = runner.crawl(spider)
    deferred.addCallback(process_decliners)
    return deferred

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
run("localhost", 8080)
