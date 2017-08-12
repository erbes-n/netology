import time
import requests
import json
from pprint import pprint

FIELDS = 'name,id,members_count'
VK_API_BASE = 'https://api.vk.com/method/'
ERR_CODE_FAST = 6
ERR_CODE_BLOCKED = 18


class VkBase:
	VERSION = "5.67"
	# TOKEN = '04f24c05f7ae8e2b9ae046a5327c06c8034b8b777800f842ae6cc93fa881bbfde5b4c2cf0e933631b966f'
	TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'

	def get_params_for_request(self, additional_params):
		params = {
			'access_token': self.TOKEN,
			'v': self.VERSION
		}
		params.update(additional_params)
		return params

	def call(self, url, params):
		while True:
			try:
				response = requests.get(url, params)
				status = response.status_code
				response.raise_for_status()
				content = response.json()
				if 'error' in content:
					if content['error']['error_code'] == ERR_CODE_FAST:
						time.sleep(1)
						continue
					else:
						response = dict()
						response['error_code'] = content['error']['error_code']
						response['info'] = content['error']['error_msg']
						break
				response = content['response']
				break
			except requests.exceptions.HTTPError as err_info:
				response = dict()
				response['error_code'] = status
				response['info'] = err_info
				break
			except TimeoutError:
				print("TimeOut...Sleep")
				time.sleep(10)
		return response


class VkGroups(VkBase):
	METHOD_INFO_GROUPS = '{}groups.getById'.format(VK_API_BASE)

	def groups_info(self, group_ids, fields=None):
		if isinstance(group_ids, list):
			groups_string = ','.join(map(str, group_ids))
		else:
			groups_string = str(group_ids)
		additional_params = {
			'group_ids': groups_string,
			'fields': fields,
		}
		params = self.get_params_for_request(additional_params)
		result_info = self.call(self.METHOD_INFO_GROUPS, params)
		return result_info


class VkUser(VkBase):
	METHOD_FRIENDS_GET = '{}friends.get'.format(VK_API_BASE)
	METHOD_USER_GET = '{}users.get'.format(VK_API_BASE)
	METHOD_GROUPS_GET = '{}groups.get'.format(VK_API_BASE)

	def __init__(self, user_id):
		self.user_id = user_id

	def get_id(self):
		additional_params = {
			'user_ids': self.user_id,
		}
		params = self.get_params_for_request(additional_params)
		response = self.call(self.METHOD_USER_GET, params)
		user_true_id = response[0]['id']
		return user_true_id

	def set_real_id(self):
		self.user_id = self.get_id()

	def friends_list(self, fields=None, order=None):
		additional_params = {
			'user_id': self.user_id,
			'fields': fields,
			'order': order
		}
		params = self.get_params_for_request(additional_params)
		response = self.call(self.METHOD_FRIENDS_GET, params)
		return response

	def groups_list(self, extended=0, fields=None, count=None):
		additional_params = {
			'user_id': self.user_id,
			'extended': extended,
			'fields': fields,
			'count': count
		}
		params = self.get_params_for_request(additional_params)
		response = self.call(self.METHOD_GROUPS_GET, params)
		return response

	def print_errors(self, response):
		if 'error_code' in response:
			if response['error_code'] == ERR_CODE_BLOCKED:
				print("Аккаунт пользователя (id - {}) заблокирован или удален".format(self.user_id))
			else:
				print('Ошибка: {0}. id: {1}. Сведения об ошибке: {2}'
						.format(response['error_code'], self.user_id, response['info']))

	def get_unique_groups_id(self):
		friends_list = self.friends_list()
		excluded_friends_id = []
		unique_groups_id = []
		if 'error_code' in friends_list:
			self.print_errors(friends_list)
		else:
			friends_list = friends_list['items']
			all_groups_set = set()
			friends_num = len(friends_list)
			for a, friend_id in enumerate(friends_list, start=1):
				if a % 20 == 0:
					print('. Обработано {} из {} друзей. Осталось {}'.format(a, friends_num, friends_num - a))
				else:
					print('.')
				vk_friend = VkUser(friend_id)
				new_groups_list = vk_friend.groups_list()
				if 'error_code' in new_groups_list:
					if new_groups_list['error_code'] == ERR_CODE_BLOCKED:
						excluded_friends_id.append(friend_id)
					else:
						vk_friend.print_errors(new_groups_list)
				else:
					all_groups_set.update(new_groups_list['items'])
			user_groups = set(self.groups_list()['items'])
			unique_groups_id = list(user_groups - all_groups_set)
		return unique_groups_id, excluded_friends_id

	def get_groups_info(self, group_ids, fields=None):
		groups_info = VkGroups().groups_info(group_ids, fields)
		group_info_list = []
		if fields is not None:
			fields = fields.split(',')
			for group in groups_info:
				group_info = {key: str(group[key]) for key in fields if key in group}
				group_info_list.append(group_info)
		else:
			group_info_list = groups_info
		return group_info_list


def create_json_file(group_info_list):
	file_name = "groups.json"
	with open(file_name, "w", encoding='utf8') as rfile:
		json.dump(group_info_list, rfile, ensure_ascii=False)


def start_run():
	first_id = input('Введите имя пользователя (screen_name) или id:')
	first_user = VkUser(first_id)
	first_user.set_real_id()
	unique_groups, blocked_ids = first_user.get_unique_groups_id()
	if not unique_groups:
		print("Нет уникальных групп для пользователя {}".format(first_id))
	else:
		un_groups_info_list = first_user.get_groups_info(unique_groups, FIELDS)
		create_json_file(un_groups_info_list)
		print("Из поиска групп были исключены заблокированные/удаленные id друзей: {}".format(blocked_ids))
		with open("groups.json", "r", encoding='utf8') as rf:
			json_object = json.load(rf)
			pprint(json_object)


if __name__ == "__main__":
	start_run()
