import requests
import os
import chardet


def create_result_directory(result_directory):
    if os.path.exists(result_directory) is True:
        result_files = [os.path.join(result_directory, file) for file in os.listdir(result_directory)]
        [os.remove(file) for file in result_files]
    else:
        os.mkdir(result_directory)


def create_file_list(extension):
    file_list = []
    for local_file_name in os.listdir(os.getcwd()):
        if local_file_name.endswith(extension):
            file_list.append(local_file_name)
    return file_list


def translate_it(path_to_text, result_path, from_lang, to_lang="ru"):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    with open(path_to_text, "rb") as source_file:
        data = source_file.read()
        file_encoding = chardet.detect(data)["encoding"]

    with open(path_to_text, encoding=file_encoding) as source_file:
        text = source_file.read()

    params = {
        'key': key,
        'lang': '{0}-{1}'.format(from_lang, to_lang),
        'text': text,
    }
    response = requests.get(url, params=params).json()

    with open(result_path, "w") as new_file:
        new_file.write(' '.join(response.get('text', [])))


EXT = "txt"
RESULT_DIR = "Result"
create_result_directory(RESULT_DIR)
translate_file_list = create_file_list(EXT)
for file in translate_file_list:
    source_path = os.path.join(os.getcwd(), file)
    res_path = os.path.join(os.getcwd(), RESULT_DIR, file)
    source_lang = file[:2].lower()
    translate_it(source_path, res_path, source_lang)
