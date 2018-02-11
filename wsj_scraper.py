from datetime import datetime, timedelta
from decimal import *
import urllib.parse as parse
from scrapy import Spider
from scrapy.http.request import Request

nyse_url = 'http://www.wsj.com/mdc/public/page/2_3021-losenyse-loser-'
nasdaq_url = 'http://www.wsj.com/mdc/public/page/2_3021-losennm-loser-'
profile_base_url = 'http://quotes.wsj.com/'

def get_previous_weekday():
    # markets are open mon-fri, weekdays
    previous_date = datetime.now() - timedelta(1)
    while previous_date.weekday() > 4:
        previous_date = previous_date - timedelta(1)

    return previous_date.strftime("%Y%m%d")

class WSJSpider(Spider):
    name = 'WSJ Spider'

    def start_requests(self):
        yesterday = get_previous_weekday()
        for u in [nyse_url, nasdaq_url]:
            url = '{}{}.html'.format(u, yesterday)
            yield Request(url=url, callback=self.parse_decliners)

    def parse_decliners(self, response):
        rows = response.xpath('//table[@class="mdcTable"]/tr')
        for row in rows[1:]:
            link = row.xpath('.//td[2]/a/@href').extract_first()
            symbol_qs = parse.parse_qs(parse.urlparse(link).query)
            symbol = symbol_qs.get('symbol')[0]
            closing_price = Decimal(row.xpath('.//td[3]/text()').extract_first().replace('$', ''))
            price_decline = Decimal(row.xpath('.//td[4]/text()').extract_first())
            price_decline_percentage = Decimal(row.xpath('.//td[5]/text()').extract_first())

            decliner = {
                'symbol': symbol,
                'closing_price': closing_price,
                'price_decline': price_decline,
                'price_decline_percentage': price_decline_percentage
            }
            yield decliner
            # fetch key ratios of symbol
            symbol_profile_url = '{}{}'.format(profile_base_url, symbol)
            yield response.follow(symbol_profile_url, self.parse_key_ratios)

    def parse_key_ratios(self, response):
        symbol = response.xpath('/html/body/div[1]/div[2]/section[1]/div[1]/div/h1/span[2]/text()').extract_first()
        pe_ratio_str = response.xpath('//*[@id="cr_keystock_drawer"]/div[1]/ul/li[1]/div/span/text()').extract_first()
        try:
            pe_ratio = Decimal(pe_ratio_str.strip())
        except:
            pe_ratio = None

        dividend_yield_str = response.xpath('//*[@id="cr_keystock_drawer"]/div[1]/ul/li[6]/div/span/text()').extract_first()
        try:
                dividend_yield = Decimal(dividend_yield_str.strip().replace('%', ''))
        except:
                dividend_yield = None

        ratios = {
            'symbol': symbol,
            'pe_ratio': pe_ratio,
            'dividend_yield': dividend_yield
        }
        yield ratios
