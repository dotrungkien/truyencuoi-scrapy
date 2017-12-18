import scrapy
import pandas as pd


class TruyencuoiSpider(scrapy.Spider):
    name = 'truyencuoi'
    start_urls = ['http://www.truyencuoihay.vn/?pagenumber=1']
    names = []
    categories = []
    contents = []
    data = pd.DataFrame()

    def parse(self, response):
        for product in response.css('div.product-item'):
            name = product.css('h2.product-title a::text').extract_first()
            category = product.css('div.product-item div.category-name a::text').extract_first()
            desc = '\n'.join(product.css('div.description p::text').extract())
            self.names.append(name)
            self.categories.append(category)
            self.contents.append(desc)
        next_page = response.css('a.next-page::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        else:
            print(len(self.names), len(self.categories), len(self.contents))
            self.data['Name'] = self.names
            self.data['Category'] = self.categories
            self.data['Content'] = self.contents
            self.data.to_csv('data/truyencuoi.csv')
