# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EeussPipeline:
    def process_item(self, item, spider):
        if spider.name == 'eeus':
            with open('1.txt', 'a+', encoding='utf-8') as f:
                f.write(item['first_m3u8'] + '----' + item['title'].strip().replace(' ', '') + '\n')
            return item
