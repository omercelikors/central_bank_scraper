class Config():
	# These are initial values.
	# This dict of list inludes all data of spiders. 
	# This dict of list maps spider names and start urls.
	SPIDER_DATAS = [
		{
			'main_datas' : {
				'spider_name' : 'informative_central_bank_rates',
				'url' : 'https://www.tcmb.gov.tr/bilgiamackur/'
			},
			'other_datas' : {
				'start_date' : '01.01.2022',
				'end_date' : '28.02.2022',
				'currency_codes' : ['UAH','DKK'],
				's3_file_name' : 'informative_central_bank_rates.xml',
			}
		},
		{
			'main_datas' : {
				'spider_name' : 'indicative_central_bank_rates',
				'url' : 'https://www.tcmb.gov.tr/kurlar/'
			},
			'other_datas' : {
				'start_date' : '01.01.2022',
				'end_date' : '28.02.2022',
				'currency_codes' : ['UAH','DKK'],
				's3_file_name' : 'indicative_central_bank_rates.xml',
			}
		}
	]