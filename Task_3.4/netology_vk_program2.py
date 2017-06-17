# from urllib.parse import urlencode
import requests


# from pprint import pprint

# AUTHORIZE_URL = "https://oauth.vk.com/authorize"

# auth_data = {
# 	'client_id': APP_ID,
# 	'response_type': 'token',
# 	'scope': "friends,status,video",
# 	'v': VERSION
# }
#
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))


def request_to_vk_api(method, access_token, version, user_id=None, fields=None, order=None):
	params = {
		'access_token': access_token,
		'v': version,
		'user_id': user_id,
		'fields': fields,
		'order': order
	}
	return requests.get(method, params)


def search_mutual_friends_by_id(requested_friends_id_list, method, access_token, version, fields=None,
								order=None):
	mutual_friends_id_set = set()
	excluded_friends = []
	new_mutual_friends_list = []
	for friend_id in requested_friends_id_list:
		try:
			new_response = request_to_vk_api(method, access_token, version, friend_id, fields, order)
			new_friends_set = set([friend['id'] for friend in new_response.json()['response']['items']])
			if len(mutual_friends_id_set) == 0:
				mutual_friends_id_set = new_friends_set
				all_friends_list = new_response.json()['response']['items']
			else:
				mutual_friends_id_set = mutual_friends_id_set & new_friends_set
				mutual_friends_id_list = list(mutual_friends_id_set)
				new_mutual_friends_list = [friend for friend in all_friends_list for friend_id in mutual_friends_id_list
											if friend['id'] == friend_id]
			# print(friend_id)
			# pprint(mutual_friends_id_set)
		except LookupError:
			excluded_friends.append(friend_id)
			continue
	new_mutual_friends_list = sorted(new_mutual_friends_list, key=lambda d: d['last_name'])
	return new_mutual_friends_list, excluded_friends


def print_friends_list(all_friends_list):
	for i, friend in enumerate(all_friends_list):
		if i == 0:
			print('{0}. {1} {2} id: {3} (введенный id)'.format(i, friend['first_name'], friend['last_name'],
																friend['id']))
		else:
			print('{0}. {1} {2} id: {3}'.format(i, friend['first_name'], friend['last_name'], friend['id']))


def print_mutual_friends(all_friends_list, requested_friends, all_mutual_friends, excluded_friends=None):
	if len(excluded_friends) > 0:
		print('Из поиска общих друзей исключены (аккаунт заблокирован):')
		for i, excluded_friend_id in enumerate(excluded_friends):
			for friend in all_friends_list:
				if friend['id'] == excluded_friend_id:
					print('{0}. {1} {2} id: {3}'.format(i + 1, friend['first_name'], friend['last_name'], friend['id']))
	print('Для друзей:')
	for excluded_friend_id in excluded_friends:
		requested_friends.remove(excluded_friend_id)
	for i, requested_friend_id in enumerate(requested_friends):
		for friend in all_friends_list:
			if friend['id'] == requested_friend_id:
				print('{0}. {1} {2} id: {3}'.format(i + 1, friend['first_name'], friend['last_name'], friend['id']))
	print("Общие друзья:")
	for i, mut_friend in enumerate(all_mutual_friends):
		print('{0}. {1} {2} id: {3}'.format(i + 1, mut_friend['first_name'], mut_friend['last_name'], mut_friend['id']))


VERSION = "5.65"
APP_ID = 6077507
SYSTEM_TOKEN = '2c61dff52c61dff52c61dff5eb2c3d63b622c612c61dff5752222b7c96858bf5c59da8d'
METHOD_FRIENDS_GET = "https://api.vk.com/method/friends.get"
METHOD_USER_GET = "https://api.vk.com/method/users.get"
FIELDS = 'nickname'
ORDER = 'name'
FIRST_ID = input('Введите id пользователя: ')

initial_response = request_to_vk_api(METHOD_USER_GET, SYSTEM_TOKEN, VERSION, FIRST_ID, FIELDS)
initial_user = initial_response.json()['response'][0]
response = request_to_vk_api(METHOD_FRIENDS_GET, SYSTEM_TOKEN, VERSION, FIRST_ID, FIELDS, ORDER)
friends_list = sorted(response.json()['response']['items'], key=lambda d: d['last_name'])
friends_list.insert(0, initial_user)
print_friends_list(friends_list)
while True:
	friend_list_for_search = input('Введите через запятую номера друзей, для которых следует найти общих друзей: ')
	friend_list_for_search = friend_list_for_search.split(",")
	friends_id_list = [friends_list[int(number)]['id'] for number in friend_list_for_search]
	search_result = search_mutual_friends_by_id(friends_id_list, METHOD_FRIENDS_GET, SYSTEM_TOKEN, VERSION, FIELDS)
	mutual_friends_list = search_result[0]
	excluded_friends_id_list = search_result[1]
	print_mutual_friends(friends_list, friends_id_list, mutual_friends_list, excluded_friends_id_list)
