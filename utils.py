import ast
import itertools
import re
import collections
import typing
import operator

Call = collections.namedtuple('Call', ['line', 'start', 'end'])

pattern = re.compile(r'[\w.]*?\((.*?)\)')


def get_calls(code: typing.Iterable[ast.stmt]) -> typing.Iterator[ast.Call]:
    def is_call(stmt: ast.stmt):
        try:
            return isinstance(stmt.value, ast.Call)
        except AttributeError:
            return False

    return map(operator.attrgetter('value'), filter(is_call, code))


def get_params(call: ast.Call):
    return call.args


def get_defs(code):
    code = reformat_code(code)
    try:
        m = ast.parse(code)
    except SyntaxError:
        return {}
    defs = collections.defaultdict(list)
    for call in get_calls(m.body):
        defs[call].append(get_params(call))
    return defs


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