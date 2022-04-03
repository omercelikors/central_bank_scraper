# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from botocore.exceptions import ClientError
import logging


class CentralBankScraperPipeline:

	def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, base_path_for_xml):
		self.aws_access_key_id = aws_access_key_id
		self.aws_secret_access_key = aws_secret_access_key
		self.bucket_name = bucket_name
		self.base_path_for_xml = base_path_for_xml
		self.all_currencies = []

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			aws_access_key_id=crawler.settings.get('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=crawler.settings.get('AWS_SECRET_ACCESS_KEY'),
			bucket_name=crawler.settings.get('BUCKET_NAME'),
			base_path_for_xml = crawler.settings.get('BASE_PATH_FOR_XML')
		)

	def open_spider(self, spider):
		pass

	def process_item(self, item, spider):
		self.all_currencies.append(item['currency'].replace(b'\n',b'').replace(b'\t',b''))
		return item

	def close_spider(self, spider):
		with open(f"{self.base_path_for_xml}{spider.other_datas['s3_file_name']}", "wb") as f:
			f.write(b''.join(self.all_currencies))
		
		# create_client_result = self.create_s3_bucket_client()

		# if create_client_result:
		#     create_s3_bucket_result = self.create_s3_bucket()
		
		# if create_s3_bucket_result:
		#     upload_file_result = self.upload_file(spider.other_datas['s3_file_name'])
		
		return True

	def create_s3_bucket_client(self):
		"""Create an S3 client

		:return: True if client created, else False
		"""

		try:
			self.s3_client = boto3.client("s3",
										  aws_access_key_id=self.aws_access_key_id, 
										  aws_secret_access_key=self.aws_secret_access_key)
		except ClientError as e:
			logging.error(e)
			return False
		
		return True

	def create_s3_bucket(self):
		"""Create an S3 bucket

		:param s3_client: s3 client
		:return: True if bucket created, else False
		"""

		try:
			response = self.s3_client.create_bucket(Bucket=self.bucket_name)
		except Exception as e:
			logging.error(e)
			return False

		return True

	def upload_file(self, file_name):
		"""Upload a file to an S3 bucket

		:param file_name: File to upload
		:param object_name: S3 object name. If not specified then file_name is used
		:return: True if file was uploaded, else False
		"""

		try:
			response = self.s3_client.upload_file(f"{self.base_path_for_xml}{file_name}", self.bucket_name, file_name)
		except Exception as e:
			logging.error(e)
			return False

		return True