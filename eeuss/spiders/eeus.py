import scrapy
from eeuss.items import EeussItem
import re


class EeusSpider(scrapy.Spider):
    name = 'eeus'
    allowed_domains = ['eeussfv.com']
    start_urls = ['https://m.eeussfw.com/cn/index32.htm']
    url = 'https://m.eeussfv.com'
    def parse(self, response):
        li_list = response.xpath("//div[@class='list mb bt']/ul/li")
        for li in li_list:
            item = EeussItem()
            href = li.xpath("./a/@href").extract_first()
            title = li.xpath("./a/@title").extract_first()
            item['href'] = self.url + href
            item['title'] = title

            yield scrapy.Request(
                url=item['href'],
                callback=self.parse_detail,
                meta={"item": item}
            )

        # 找到下一页
        next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                url=self.url + next_url,
                callback=self.parse
            )

    def parse_detail(self, response):   # 处理详情
        item = response.meta["item"]
        play_list = response.xpath("//div[@class='playlist']/ul/ul/li[1]/a/@href").extract_first()
        if play_list is not None:
            item['url'] = self.url + play_list
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_first_m3u8_js,
                meta={"item": item}
            )

    def parse_first_m3u8_js(self, response):    # 访问js文件，获取m3u8下载地址
        item = response.meta["item"]
        first_m3u8_js = response.xpath("//div[@class='player']/script/@src").extract_first()
        if first_m3u8_js is not None:
            item["first_m3u8_js"] = self.url + first_m3u8_js
            yield scrapy.Request(
                url=item["first_m3u8_js"],
                callback=self.parse_get_first_m3u8,
                meta={"item": item}
            )

    def parse_get_first_m3u8(self, response):   # 提取第一层m3u8文件地址并提交访问
        item = response.meta["item"]
        res = response.body.decode(response.encoding)
        if response.text is not None:
            ret = re.search(r"\$(?P<link>http.*?)\$", res)
            if ret is not None:
                item['first_m3u8'] = ret.group('link')
                yield item
    # 由于以下请求超出了start_url，注释了
    #             yield scrapy.Request(
    #                 url=item['first_m3u8'],
    #                 callback=self.parse_get_ts_from_m3u8,
    #                 meta={"item": item}
    #             )
    #
    # def parse_get_ts_from_m3u8(self, response):     # 从第一层m3u8中获取真正的m3u8
    #     item = response.meta["item"]
    #     res = response.body.decode(response.encoding)
    #     if res is not None:
    #         print(res)
    #     else:
    #         print('None')