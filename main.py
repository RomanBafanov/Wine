import os
import argparse
import collections
import datetime
import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


YEAR_OF_FOUNDATION = 1920


def formation_information_wine(wine_table, name, category):
    drink = {}
    drink['Категория'] = category[name]
    for key in wine_table.keys():
        if type(wine_table[key][name]) == float:
            drink[key] = None
        else:
            drink[key] = wine_table[key][name]

    return drink


def generate_correct_date():
    now_year = datetime.datetime.now().year
    count_years = now_year - YEAR_OF_FOUNDATION
    last_digit = count_years % 10
    last_two_digits = count_years % 100

    if 11 <= last_two_digits <= 14:
        year = f'{count_years} лет'
    elif last_digit == 1:
        year = f'{count_years} год'
    elif 2 <= last_digit <= 4:
        year = f'{count_years} года'
    else:
        year = f'{count_years} лет'

    return year


def launch_website(year, drinks_for_website):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        year=year,
        drinks=drinks_for_website,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        description='Сайт магазина авторского вина "Новое русское вино".'
                    'Для запуска вам понадобится файл с ассортиментом вина:'
                    'Наберите команду python main.py Файл с ассортиментом.'
                    'Если вы не укажете файл, то будет выбран файл-пример из проекта.')
    parser.add_argument('excel_file', nargs='?', default='wine_store.xlsx', help='Файл с ассортиментом')
    args = parser.parse_args()
    wine_store = os.path.abspath(args.excel_file)
    excel_data_df = pandas.read_excel(io=wine_store)
    wine_table = excel_data_df.to_dict()
    categories = wine_table['Категория']

    drinks_for_website = collections.defaultdict(list)
    for name in categories:
        next_drink = formation_information_wine(wine_table, name, categories)
        drinks_for_website[categories[name]].append(next_drink)

    year = generate_correct_date()

    launch_website(year, drinks_for_website)


if __name__ == '__main__':
    main()
