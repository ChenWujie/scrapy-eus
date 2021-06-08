# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class EeussItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class EeussItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    href = scrapy.Field()
    video_url = scrapy.Field()
    first_m3u8 = scrapy.Field()
    m3u8 = scrapy.Field()
    first_m3u8_js = scrapy.Field()