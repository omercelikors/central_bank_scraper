from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import create_log
from config import Config
from datetime import datetime


class Runner(Config):

	def start_log_record(self):
		# my_log module produces spider logs to logs folder in project.
		return create_log.init(datetime.utcnow())

	def start_crawl(self):
		try:
			# This block runs multiple spiders simultaneously.
			process = CrawlerProcess (get_project_settings())

			for spider_data in self.SPIDER_DATAS:
				process.crawl(spider_data['main_datas']['spider_name'],
							  start_url = spider_data['main_datas']['url'],
							  other_datas = spider_data['other_datas'])

			process.start() # here blocks code
			return True
		except:
			return False

	def run(self):
		log_file_name = self.start_log_record()
		spider_result = self.start_crawl()
		return spider_result

if __name__ == "__main__":
	runner = Runner()
	runner.run()