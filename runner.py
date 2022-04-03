from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import create_log
from config import Config
from datetime import datetime


class Runner(Config):

	def start_log_record(self):
		# create_log module produces spider logs to logs folder in project.
		return create_log.init(datetime.utcnow())

	def start_crawl(self):
		try:
			# This block runs multiple spiders simultaneously.
			configure_logging()
			settings = get_project_settings()
			runner = CrawlerRunner(settings)
			
			for spider_data in self.SPIDER_DATAS:
				runner.crawl(spider_data['main_datas']['spider_name'],
							  start_url = spider_data['main_datas']['url'],
							  other_datas = spider_data['other_datas'])

			d = runner.join()
			d.addBoth(lambda _: reactor.stop())
			reactor.run() # The script will block here until all crawling jobs are finished.

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