import re
import os
import errno


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
    paras = re.findall('\[([^\[\]]*)\]', call[1])
    return {'target': target,
            'paras': paras}
