# -*- coding:utf-8 -*-
# all 一假为假


def all(iterable):
    for x in iterable:
        if not x:
            return False

    return True


# any 一真为真

def any(iterable):
    for x in iterable:
        if x:
            return True
    return False
