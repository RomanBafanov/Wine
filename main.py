import collections
import datetime
import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


excel_data_df = pandas.read_excel(io='wine_store.xlsx')
wine_table = excel_data_df.to_dict()
categoryes = wine_table['Категория']


def formation_information_wine(name, category):
    drink = {}
    drink['Категория'] = category[name]
    for key in wine_table.keys():
        if type(wine_table[key][name]) == float:
            drink[key] = None
        else:
            drink[key] = wine_table[key][name]

    return drink


drinks_for_website = collections.defaultdict(list)
for name in categoryes:
    next_drink = formation_information_wine(name, categoryes)
    drinks_for_website[categoryes[name]].append(next_drink)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def generate_correct_date(years):
    last_digit = years % 10
    last_two_digits = years % 100

    if 11 <= last_two_digits <= 14:
        year = f'{years} лет'
    elif last_digit == 1:
        year = f'{years} год'
    elif 2 <= last_digit <= 4:
        year = f'{years} года'
    else:
        year = f'{years} лет'

    return year


now_year = datetime.datetime.now().year
count_years = now_year - 1920
year = generate_correct_date(count_years)

rendered_page = template.render(
    year=year,
    drinks=drinks_for_website,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
