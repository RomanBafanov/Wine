import collections
import datetime
import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


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
    count_years = now_year - 1920
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


def main():
    excel_data_df = pandas.read_excel(io='wine_store.xlsx')
    wine_table = excel_data_df.to_dict()
    categoryes = wine_table['Категория']

    drinks_for_website = collections.defaultdict(list)
    for name in categoryes:
        next_drink = formation_information_wine(wine_table, name, categoryes)
        drinks_for_website[categoryes[name]].append(next_drink)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    year = generate_correct_date()

    rendered_page = template.render(
        year=year,
        drinks=drinks_for_website,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
