import osa
import os
from math import *

TEMPS_FILE = 'temps.txt'
CURRENCIES_FILE = 'currencies.txt'
TRAVEL_FILE = 'travel.txt'


def average_temp_in_celsius(path_to_file):
	url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
	client = osa.client.Client(url)
	scale_dict = {
		'C': 'degreeCelsius',
		'F': 'degreeFahrenheit',
		'Re': 'degreeRankine',
		'Ra': 'degreeReaumur',
		'K': 'kelvin'
	}
	with open(path_to_file) as f:
		temps = []
		for line in f:
			temp_unit = line.split()
			response = client.service.ConvertTemp(Temperature=float(temp_unit[0]),
												  FromUnit=scale_dict[temp_unit[1]],
												  ToUnit=scale_dict['C'])
			temps.append(response)
	average_temp = round(sum(temps)/len(temps), 1)
	return average_temp


def convert_sums_of_currencies(path_to_file):
	url = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
	client = osa.client.Client(url)
	with open(path_to_file) as f:
		sum_costs = 0
		for line in f:
			cost_unit = line.split()
			response = client.service.ConvertToNum(fromCurrency=cost_unit[2],
													toCurrency='RUB',
													amount=float(cost_unit[1]),
													rounding=True)
			sum_costs += response
	return ceil(sum_costs)


def convert_miles_to_km(path_to_file):
	url = 'http://www.webservicex.net/length.asmx?WSDL'
	client = osa.client.Client(url)
	with open(path_to_file) as f:
		total_trip_length = 0
		for line in f:
			flight_length = line.split()
			flight_length[1] = flight_length[1].replace(',', '')
			response = client.service.ChangeLengthUnit(LengthValue=float(flight_length[1]),
														fromLengthUnit='Miles',
														toLengthUnit='Kilometers')
			total_trip_length += response
	return round(total_trip_length, 2)


temps_file = os.path.join(os.getcwd(), TEMPS_FILE)
currencies_file = os.path.join(os.getcwd(), CURRENCIES_FILE)
travel_file = os.path.join(os.getcwd(), TRAVEL_FILE)

av_temp = average_temp_in_celsius(temps_file)
trip_cost = convert_sums_of_currencies(currencies_file)
trip_length = convert_miles_to_km(travel_file)

print('{0}° C'.format(av_temp))
print('{0} руб.'.format(trip_cost))
print('{0} км.'.format(trip_length))