# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CentralBankScraperPipeline:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.all_currencies = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            aws_access_key_id=crawler.settings.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=crawler.settings.get('AWS_SECRET_ACCESS_KEY'),
            region=crawler.settings.get('REGION')
        )

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.all_currencies.append(item['currency'].replace(b'\n',b'').replace(b'\t',b''))
        return item

    def close_spider(self, spider):
        with open(spider.other_datas['s3_file_name'], "wb") as f:
            f.write(b''.join(self.all_currencies))