import json
import chardet
from collections import Counter
import xml.etree.ElementTree as ET
import codecs
import os


def choose_file():
    i = 0
    file_list = []
    for file_name in os.listdir(os.getcwd()):
        if file_name.endswith("json") or file_name.endswith("xml"):
            file_list.append(file_name)
            i += 1
            print(i, file_name)
    file_number = int(input("Выберите номер файла из списка: "))
    file_name = file_list[file_number - 1]
    return file_name

def detect_file_type(file_name):
    if file_name[-4:] == "json":
        file_type = "json"
    elif file_name[-3:] == "xml":
        file_type = "xml"
    return file_type

def create_json_text_list(file_name):
    with open(file_name, "rb") as news_file:
        data = news_file.read()
        result = chardet.detect(data)["encoding"]
        json_object = json.loads(data.decode(result))
        text_list = []
        news_list = json_object["rss"]["channel"]["item"]
        for news_item in news_list:
            if type(news_item["description"]) is str:
                news_text = news_item["description"]
            else:
                news_text = news_item["description"]["__cdata"]
            text_list.append(news_text)
    return text_list

def create_xml_text_list(file_name):
    with open(file_name, "rb") as news_file:
        data = news_file.read()
        result = chardet.detect(data)["encoding"]
        string = data.decode(result)
        n_tree = ET.fromstring(string)
        text_list = []
    for item in n_tree.iterfind('./channel/item/description'):
        text_list.append(item.text)
    return text_list

def remove_punctuation(text):
    punct = ("!", ",", "?", ".", "(", ")", ":", ";", '"', "'", "/", "«", "»")
    translation_table = dict.fromkeys(map(ord, punct), " ")
    return text.translate(translation_table)

def delete_text(text, start_symbol, end_symbol):
    open_index = text.find(start_symbol)
    while open_index > -1:
        close_index = text.find(end_symbol, open_index + len(start_symbol)) + 1
        if close_index < open_index:
            close_index = open_index + len(start_symbol)
        text = text.replace(text[open_index:close_index], "")
        open_index = text.find(start_symbol)
    return text

def create_news_words_list(text_list):
    words_list = []
    for text in text_list:
        news_text = delete_text(text, "<br>/", "/")
        news_text = delete_text(news_text, "<", ">")
        news_text = remove_punctuation(news_text)
        news_words = news_text.lower().split()
        news_words = [word.strip() for word in news_words]
        words_list.extend(news_words)
    return words_list

def top_word_frequency(words_list, top_depth = 10, min_word_length = 6):
    long_words = [word for word in words_list if len(word) > min_word_length]
    most_common_words = Counter(long_words).most_common(top_depth)
    return most_common_words

def print_top(most_common_words):
    print("Для файла {0}:".format(file_name))
    print("Частота употребления {0} самых используемых слов:".format(len(most_common_words)))
    for i, word in enumerate(most_common_words):
        print("{0}. {1} - {2} раз(а)".format(i + 1, word[0], word[1]))


file_name = choose_file()
file_type = detect_file_type(file_name)
if file_type == "json":
    text_list = create_json_text_list(file_name)
elif file_type == "xml":
    text_list = create_xml_text_list(file_name)
words_list = create_news_words_list(text_list)
top = top_word_frequency(words_list, 10, 6)
print_top(top)
