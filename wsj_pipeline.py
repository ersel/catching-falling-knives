from simplejson import dump

class StocksPipeline(object):
    def __init__(self):
        self.symbols = {}

    def process_item(self, item, spider):
        if len(item.keys()) == 4:
            # add symbol to dict
            self.symbols[item['symbol']] = item
        elif len(item.keys()) == 3:
            # merge ratio data
            symbol_data = self.symbols[item['symbol']]
            merged_data = {**symbol_data, **item}
            self.symbols[item['symbol']] = merged_data

    def close_spider(self, spider):
        with open('decliners.json', 'w') as output:
            dump(self.symbols, output, sort_keys=True, indent=4, use_decimal=True)
