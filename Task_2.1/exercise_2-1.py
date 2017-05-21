def open_cook_book(file_name):
    cook_book = {}
    with open(file_name, encoding = "utf8") as cb:
        headers = cb.readline().lower().split("|")
        key_names = [header.strip() for header in headers]
        for line in cb:
            if not line.isspace():
                dish_name = line.lower().strip()
                ingridients_quantity = int(cb.readline())
                ingridients = []
                for number in range(ingridients_quantity):
                    nline = cb.readline().strip().lower().split("|")
                    ingridient_values = [value.strip() for value in nline]
                    ingridient_values[1] = int(ingridient_values[1])
                    ingridient = {key_name: value for key_name, value in zip(key_names, ingridient_values)}
                    ingridients.append(ingridient)
                cook_book[dish_name] = ingridients
    return cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
            new_shop_list_item = dict(ingridient)
            new_shop_list_item['quantity'] *= person_count
            if new_shop_list_item['ingridient_name'] not in shop_list:
                shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
            else:
                shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
    return shop_list

def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print('{ingridient_name} {quantity} {measure}'.format(**shop_list_item))

def create_shop_list(cook_book):
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите количество блюд в расчете на одного (через запятую): ').strip().lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)

cook_book = open_cook_book("cook_book.txt")
create_shop_list(cook_book)
