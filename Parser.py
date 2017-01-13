from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import datetime


MAIN_URL = 'https://freelancehunt.com'
BASE_URL = 'https://freelancehunt.com/projects/skill/veb-programmirovanie/99.html'
LAST_PAGE = '?page=99'


def get_html(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(request).read()


def get_page_count():
    # get_html(BASE_URL + LAST_PAGE)
    soup = BeautifulSoup(get_html(BASE_URL + LAST_PAGE), 'html.parser')
    return int(soup.find('div', class_='pagination').find_all('li')[-2].find('a').text)


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='table table-normal')
    rows = table.find_all('tr')[1:]

    projects = []

    for row in rows:
        cols = row.find_all('td')
        if cols.__len__() < 3:
            continue

        categories = ''
        small = cols[0].div.find('small')

        if small:
            categories = str(small.text).replace('<strong>', '').\
                replace('</strong>', '')

        time = cols[3].div.h2.text
        time_month = cols[3].div.find('h5')
        if time_month:
            time = time + " " + time_month.text

        projects.append({
            'title': cols[0].a.text,
            'categories': categories,
            'price': cols[1].span.text.strip(),
            'application': cols[2].a.text,
            'time': time,
            'final_date': cols[4].div.h2.text + " " + cols[4].div.h5.text,
            'link': MAIN_URL + cols[0].a.get('href')
        })

    return projects


def save(projects):
    current_date = datetime.datetime.now()
    filename = 'result_' + current_date.strftime('%d%m%Y_%H%M%S') + '.csv'
    with open(filename, 'x', encoding='utf-16', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("Проэкт", 'Категории', 'Цена', 'Заявки',
                         'Открыт', 'Актуален', 'Ссылка'))

        writer.writerow(())

        for project in projects:
            writer.writerow((project['title'], project['categories'],
                             project['price'], project['application'],
                             project['time'], project['final_date'],
                             project['link']))


def main():
    page_count = get_page_count()
    print('Found {} pages'.format(page_count))

    projects = []

    for page in range(1, page_count):
        print('Parsing... {:.1%}'.format(page/page_count))
        projects.extend(parse(get_html(BASE_URL + ('?page={}'.format(page)))))

    save(projects)
    print('Parsing... 100%')
    print('Done!')

if __name__ == '__main__':
    main()
