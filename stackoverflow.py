import ast
import collections
import itertools

import bs4
import requests

import utils


def reformat_code(old_code):
    """Moves imports to top."""

    def line_type(line: str):
        if line.startswith('import ') or line.startswith('from '):
            return 'import'
        else:
            return 'code'

    new_code = ''
    for _, g in itertools.groupby(sorted(old_code.split('\n'), key=line_type, reverse=True), key=line_type):
        g = list(filter(str.strip, g))
        new_code += '\n'.join(g) + '\n'

    return new_code


def get_codes(element):
    for answer in element.find_all(class_='answer'):
        yield '\n'.join(c.text for c in answer.find_all('code'))


def get_defs(code):
    code = reformat_code(code)
    try:
        m = ast.parse(code)
    except SyntaxError:
        return {}
    defs = collections.defaultdict(list)
    for call in utils.get_calls(m.body):
        defs[call].append(utils.get_params(call))
    return defs


if __name__ == '__main__':
    r = requests.get('https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-using-python')
    soup = bs4.BeautifulSoup(r.text, 'lxml')

    for code in itertools.islice(get_codes(soup), 100):
        defs = get_defs(code)
        print(defs)
        print()
