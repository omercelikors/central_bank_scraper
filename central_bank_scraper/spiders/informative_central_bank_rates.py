import scrapy
import json
import logging
import sys
from central_bank_scraper.shared_methods import SharedMethods
from scrapy.selector import Selector
import xml.etree.ElementTree as ET
from central_bank_scraper.items import CentralBankScraperItem

class InformativeCentralBankRatesSpider(scrapy.Spider, SharedMethods):
	name = "informative_central_bank_rates"

	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		# 'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://www.tcmb.gov.tr/bilgiamackur/kurlar_tr.html',
		'Connection': 'keep-alive',
		# Requests sorts cookies= alphabetically
		# 'Cookie': '_ga=GA1.3.1297059882.1648739891; TS01ab7d04=015d31d6914b44ea0522cbf2dc4c6c18a75332c3d409306e73b611697e09761eb65b0d6eee704f0d25642585eb53d029ef49421ca3; _gid=GA1.3.1278649701.1648892505',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-User': '?1',
		# 'If-Modified-Since': 'Tue, 01 Mar 2022 12:30:01 GMT',
		# 'If-None-Match': '"22d0-5d92752e14440"',
		'Cache-Control': 'max-age=0',
	}

	def start_requests(self):
		all_dates = self.get_all_dates(self.other_datas['start_date'], self.other_datas['end_date'])

		for date in all_dates:
			splitted_date = date.split('.')
			day_number = splitted_date[0]
			month_number = splitted_date[1]
			year_number = splitted_date[2]
			url_path = f"{year_number}{month_number}/{day_number}{month_number}{year_number}.xml"
			target_url = f"{self.start_url}{url_path}"

			request = scrapy.Request(url=target_url,
								 	 callback=self.parse,
									 headers=self.HEADERS)
			yield request

	def parse(self, response):
		tree = ET.ElementTree(ET.fromstring(response.text))
		root = tree.getroot()

		currency_date = root.attrib['Tarih']

		for currency in root.findall("./Currency"):
			currency_code = currency.attrib['CurrencyCode']
			if currency_code in self.other_datas['currency_codes']:
				currency.set('Tarih',currency_date)
				currency_item = CentralBankScraperItem(currency= ET.tostring(currency))
				yield currency_item