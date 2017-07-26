import ast
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
