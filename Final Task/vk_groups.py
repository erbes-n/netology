import time
import requests
import os
import json
import sys
from pprint import pprint


class VkBase:
	VERSION = "5.67"
	TOKEN = '04f24c05f7ae8e2b9ae046a5327c06c8034b8b777800f842ae6cc93fa881bbfde5b4c2cf0e933631b966f'
	# TOKEN = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'

	def get_params_for_request(self, additional_params):
		params = {
			'access_token': self.TOKEN,
			'v': self.VERSION
		}
		params.update(additional_params)
		return params


class VkGroups(VkBase):
	METHOD_INFO_GROUPS = "https://api.vk.com/method/groups.getById"

	def groups_info(self, group_ids, fields=None):
		groups_string = ''
		if type(group_ids) == list:
			for group_id in group_ids:
				groups_string += str(group_id) + ','
		else:
			groups_string = str(group_ids)
		additional_params = {
			'group_ids': groups_string,
			'fields': fields,
		}
		params = self.get_params_for_request(additional_params)
		while True:
			try:
				response = requests.get(self.METHOD_INFO_GROUPS, params)
				break
			except TimeoutError:
				print("TimeOut...Sleep")
				time.sleep(10)
		result_info = response.json()['response']
		return result_info


class VkUser(VkBase):
	METHOD_FRIENDS_GET = "https://api.vk.com/method/friends.get"
	METHOD_USER_GET = "https://api.vk.com/method/users.get"
	METHOD_GROUPS_GET = "https://api.vk.com/method/groups.get"

	def __init__(self, user_id):
		self.user_id = user_id

	def get_id(self):
		additional_params = {
			'user_ids': self.user_id,
		}
		params = self.get_params_for_request(additional_params)
		while True:
			try:
				response = requests.get(self.METHOD_USER_GET, params)
				break
			except TimeoutError:
				print("TimeOut...Sleep")
				time.sleep(10)
		user_true_id = response.json()['response'][0]['id']
		return user_true_id

	def friends_list(self, fields=None, order=None):
		self.user_id = self.get_id()
		additional_params = {
			'user_id': self.user_id,
			'fields': fields,
			'order': order
		}
		params = self.get_params_for_request(additional_params)
		response = requests.get(self.METHOD_FRIENDS_GET, params)
		while 'error' in response.json() and response.json()['error']['error_code'] == 6:
				time.sleep(1)
				response = requests.get(self.METHOD_FRIENDS_GET, params)
		while True:
			try:
				friends_list = response.json()['response']['items']
				break
			except LookupError as err_info:
				if response.json()['error']['error_code'] == 18:
					print("Аккаунт пользователя (id - {}) заблокирован или удален".format(self.user_id))
					sys.exit(1)
				else:
					print('Сведения об исключении:', err_info)
					sys.exit(1)
			except TimeoutError:
				print("TimeOut...Sleep")
				time.sleep(10)
		return friends_list

	def groups_list(self, extended=0, fields=None, count=None):
		additional_params = {
			'user_id': self.user_id,
			'extended': extended,
			'fields': fields,
			'count': count
		}
		params = self.get_params_for_request(additional_params)
		response = requests.get(self.METHOD_GROUPS_GET, params)
		result_list = []
		while 'error' in response.json() and response.json()['error']['error_code'] == 6:
			time.sleep(1)
			response = requests.get(self.METHOD_GROUPS_GET, params)
		while True:
			try:
				result_list = response.json()['response']['items']
				break
			except LookupError as err_info:
				if response.json()['error']['error_code'] == 18:
					result_list = ['blocked']
					break
				else:
					print('Сведения об исключении:', err_info)
					break
			except TimeoutError:
				print("TimeOut...Sleep")
				time.sleep(10)
		return result_list

	def get_unique_groups_id(self):
		friends_list = self.friends_list()
		all_groups_list = []
		excluded_friends_id = []
		a = 0
		friends_num = len(friends_list)
		for friend_id in friends_list:
			a += 1
			if a % 20 == 0:
				print('. Обработано {} из {} друзей. Осталось {}'.format(a, friends_num, friends_num - a))
			else:
				print('.')
			vk_friend = VkUser(friend_id)
			new_groups_list = vk_friend.groups_list()
			if 'blocked' not in new_groups_list:
				all_groups_list.extend(new_groups_list)
			else:
				excluded_friends_id.append(friend_id)
		all_groups_set = set(all_groups_list)
		user_groups = set(self.groups_list())
		unique_groups_id = list(user_groups - all_groups_set)
		return unique_groups_id, excluded_friends_id

	def get_groups_info(self, group_ids, fields=None):
		groups_info = VkGroups().groups_info(group_ids, fields)
		group_info_list = []
		if fields is not None:
			fields = fields.split(',')
			for group in groups_info:
				group_info = {key: str(group[key]) for key in fields if key in group.keys()}
				group_info_list.append(group_info)
		else:
			group_info_list = groups_info
		return group_info_list


def create_json_file(group_info_list):
	file_name = "groups.json"
	path_to_file = os.path.join(os.getcwd(), file_name)
	with open(path_to_file, "w", encoding='utf8') as rfile:
		json.dump(group_info_list, rfile, ensure_ascii=False)


FIELDS = 'name,id,members_count'

first_id = input('Введите имя пользователя (screen_name) или id:')
first_user = VkUser(first_id)
unique_groups = first_user.get_unique_groups_id()[0]
un_groups_info_list = first_user.get_groups_info(unique_groups, FIELDS)
create_json_file(un_groups_info_list)

with open(os.path.join(os.getcwd(), "groups.json"), "r", encoding='utf8') as rf:
	my_json = rf.read()
	json_object = json.loads(my_json)
	pprint(json_object)
