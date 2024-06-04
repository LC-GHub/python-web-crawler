# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeslacrawlerItem(scrapy.Item):
    main_content = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    url = scrapy.Field()
    full_html = scrapy.Field()