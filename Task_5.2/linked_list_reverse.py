"""
Домашнее задание для лекции "Задачки на собеседованиях для продвинутых,
с тонкостями языка"

Описание
	Перестроить заданный связанный список (LinkedList) в обратном порядке.
	Для этого использовать метод `LinkedList.reverse()`, представленный
	в данном файле

Примечание
	Проверить работоспособность решения можно при помощи тестов,
	которые можно запустить следующей командой:

	python3 -m unittest linked_list_reverse.py
"""

import unittest

from typing import Iterable


class LinkedListNode:

	def __init__(self, data):
		self.data = data
		self.next = None  # type: LinkedListNode

	def link(self, node: 'LinkedListNode') -> None:
		self.next = node


class LinkedList:

	def __init__(self, values: Iterable):
		previous = None
		self.head = None
		for value in values:
			current = LinkedListNode(value)
			if previous:
				previous.link(current)
			self.head = self.head or current
			previous = current

	def __iter__(self):
		current = self.head
		while current:
			yield current.data
			current = current.next

	def reverse(self) -> None:
		previous = None
		current = self.head
		while current is not None:
			next = current.next
			current.next = previous
			previous = current
			current = next
		self.head = previous
		# raise NotImplementedError

	def printList(self):
		temp = self.head
		while temp:
			print(temp.data)
			temp = temp.next


class LinkedListTestCase(unittest.TestCase):

	def test_reverse(self):
		cases = dict(
			empty=dict(
				items=[],
				expected_items=[],
			),
			single=dict(
				items=[1],
				expected_items=[1],
			),
			double=dict(
				items=[1, 2],
				expected_items=[2, 1],
			),
			triple=dict(
				items=[1, 2, 3],
				expected_items=[3, 2, 1],
				# items=[x for x in range(10000000)],
				# expected_items=[x for x in range(10000000)][::-1],
			),
		)
		for case, data in cases.items():
			with self.subTest(case=case):
				linked_list = LinkedList(data['items'])
				linked_list.reverse()
				self.assertListEqual(
					data['expected_items'],
					list(linked_list),
				)
