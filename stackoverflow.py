import itertools

import bs4
import requests

from utils import get_defs


def get_codes(element):
    for answer in element.find_all(class_='answer'):
        yield '\n'.join(c.text for c in answer.find_all('code'))


if __name__ == '__main__':
    r = requests.get('https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-using-python')
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    for code in itertools.islice(get_codes(soup), 100):
        defs = get_defs(code)
        print(defs)
        print()
