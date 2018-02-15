import sys

from .tf.boxes.ttypes import ServiceException

def ask_sure(hint):
    ans = input('Are you sure to continue to {}, y or N ? '.format(hint))
    ans = ans.upper()
    if ans == 'Y':
        return True
    return False


def report_err(e):
    print('Error: {}'.format(e), file=sys.stderr)


class InnerPathFormatException(Exception):

    def __init__(self):
        super(InnerPathFormatException, self).__init__('Inner path format is wrong')


def parse_inner_path(i):
    splited = i.split(':')
    if len(splited) < 2:
        raise InnerPathFormatException()
    return int(splited[0]), splited[1]


def report_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ServiceException as se:
            report_err('{}: {}'.format(se.op, se.why))
        except Exception as e:
            report_err(e)
    return wrapper
