import yaml

def open_cook_book_yml(file_name):
    with open(file_name, encoding = "utf8") as cb:
        new_cb = yaml.load(cb)
        cook_book = {dish.lower().strip(): value for dish, value in zip(new_cb.keys(), new_cb.values())}
        for dish in cook_book:
            for i, ingr in enumerate(cook_book[dish]):
                ingr = {key: value.lower().strip() for key, value in zip(ingr.keys(), ingr.values()) if key != "quantity"}
                for key in ingr:
                    cook_book[dish][i][key] = ingr[key]
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

cook_book = open_cook_book_yml("cook_book.yml")
create_shop_list(cook_book)
