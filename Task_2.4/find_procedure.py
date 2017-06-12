# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...


import glob
import os.path


def search_all_files_by_type(path, file_extension):
	files_list = glob.glob(os.path.join(path, "*.{}".format(file_extension)))
	return files_list


def search_files_by_text(file_names):
	text_for_search = input("Введите текст для поиска(для выхода введите 'q'): ")
	while text_for_search != "q":
		new_file_names = []
		for file in file_names:
			with open(file) as f:
				if text_for_search in f.read():
					new_file_names.append(file)
					print(file)
		file_names = new_file_names
		print("Всего файлов найдено: ", len(file_names))
		text_for_search = input("Введите текст для поиска(для выхода введите 'q'): ")

migrations = 'Migrations'
file_type = "sql"
files = search_all_files_by_type(migrations, file_type)
search_files_by_text(files)
