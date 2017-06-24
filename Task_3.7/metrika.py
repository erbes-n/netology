from _datetime import datetime, date, timedelta
from pprint import pprint
from urllib.parse import urlencode
import requests

# AUTHORIZATION_URL = 'https://oauth.yandex.ru/authorize'
# APP_ID = '7f6e2ff4e0c44a0cb51c3f927d0d8e77'
#
# auth_data = {
# 	'response_type': 'token',
# 	'client_id': APP_ID
# }

# print('?'.join((AUTHORIZATION_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAMchE3AARhiZWttpngJk7muBt9U1ZXlSE'


class MetrikaBase:
	API_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
	API_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
	token = None

	def __init__(self, token):
		self.token = token

	def get_headers(self):
		return {
			'Authorization': 'OAuth {0}'.format(self.token),
			'Content-Type': 'application/json'
		}


class YandexMetrika(MetrikaBase):

	def get_counters(self):
		headers = self.get_headers()
		r = requests.get(self.API_MANAGEMENT_URL + 'counters', headers=headers)
		return [
			Counter(self.token, counter['id']) for counter in r.json()['counters']
		]


class Counter(MetrikaBase):
	def __init__(self, token, counter_id):
		self.counter_id = counter_id
		super().__init__(token)

	def get_visits(self, period_by_days):
		headers = self.get_headers()
		params = {
			'id': self.counter_id,
			'metrics': 'ym:s:visits',
			'date1': '{}'.format(date.today() - timedelta(days=period_by_days))
		}
		r = requests.get(self.API_STAT_URL + 'data', params, headers=headers)
		return r.json()['data'][0]['metrics'][0]

	def get_pageviews(self, period_by_days):
		headers = self.get_headers()
		params = {
			'id': self.counter_id,
			'metrics': 'ym:s:pageviews',
			'date1': '{}'.format(date.today()-timedelta(days=period_by_days))
		}
		r = requests.get(self.API_STAT_URL + 'data', params, headers=headers)
		return r.json()['data'][0]['metrics'][0]

	def get_users(self, period_by_days):
		headers = self.get_headers()
		params = {
			'id': self.counter_id,
			'metrics': 'ym:s:users',
			'date1': '{}'.format(date.today() - timedelta(days=period_by_days))
		}
		r = requests.get(self.API_STAT_URL + 'data', params, headers=headers)
		return r.json()['data'][0]['metrics'][0]

metrika = YandexMetrika(TOKEN)
counter = metrika.get_counters()[0]

sample_period = 30
print('{0} визитов за {1} дней'.format(int(counter.get_visits(sample_period)), sample_period))
print('{0} просмотров за {1} дней'.format(int(counter.get_pageviews(sample_period)), sample_period))
print('{0} посетителей за {1} дней'.format(int(counter.get_users(sample_period)), sample_period))

