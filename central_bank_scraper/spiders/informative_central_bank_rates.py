# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import sys

class Informative_Central_Bank_Rates_Spider(scrapy.Spider):
	name = "informative_central_bank_rates"

	def start_requests(self):
		logging.info(self.start_url)
		logging.info(self.other_datas)
		# request = scrapy.Request(url=url_items['start_url'],
		# 						 callback=self.get_variants)
		# yield request

	def parse(self, response):
		pass