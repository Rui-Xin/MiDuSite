import MDvar


class MDEntry(object):
    'The object properties reading from .md files'
    meta = {}

    def __init__(self, fname):
        with open(fname) as f:
            lines = f.readlines()
            print 'processing ' + fname
            l = 0

            try:
                while '```MiDuSite\n' not in lines[l]:
                    l += 1
                l1 = l
                while '```\n' not in lines[l]:
                    l += 1
                l2 = l
            except IndexError:
                l1 = 0
                l2 = 0

            for line in lines[l1+1:l2]:
                info = line.split(':')
                self.meta[info[0].strip(' ')] = info[1].strip(' ').strip('"')

            self.meta['content'] = ''.join(lines[l2+1:])

    def get_mdvar(self):
        return MDvar.MDvar(_local=self.meta)
