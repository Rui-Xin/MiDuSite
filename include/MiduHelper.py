import re
import os
import errno
import MDEntry
from collections import OrderedDict


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def parseVar(inputs):
    call = re.match('([^\[]*)(.*)', inputs).groups()
    target = call[0]
    paras_raw = re.findall('\[([^\[\]]*)\]', call[1])

    paras = {}
    for para in paras_raw:
        try:
            para_info = para.split(':')
            paras[para_info[0]] = para_info[1]
        except IndexError:
            print 'parameter ' + para + ' format wrong.'

    return {'target': target,
            'paras': paras}


def od_prev_entry_meta(dic, key):
    if not isinstance(dic, OrderedDict):
        return None

    if key not in dic.keys():
        return None

    if dic.keys().index(key) - 1 < 0:
        return None

    new_index = dic.keys()[dic.keys().index(key) - 1]
    if isinstance(dic[new_index], MDEntry.MDEntry):
        return dic[new_index].meta
    else:
        return None


def od_next_entry_meta(dic, key):
    if not isinstance(dic, OrderedDict):
        return None

    if key not in dic.keys():
        return None

    try:
        new_index = dic.keys()[dic.keys().index(key) - 1]
    except IndexError:
        return None

    if isinstance(dic[new_index], MDEntry.MDEntry):
        return dic[new_index].meta
    else:
        return None
