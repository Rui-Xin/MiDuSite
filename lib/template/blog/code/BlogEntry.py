import time

MIN_META_LIST = ['title', 'date', 'tag']


class BlogItem:
    'The object of a single blog, reading from .md files'
    title = 'Untitled'
    date = time.gmtime()
    tag = []
    content = []

    def __init__(self, fname):
        with open(fname) as f:
            lines = f.readlines()
            print 'processing ' + fname
            try:
                l1 = lines.index('```MDudeInfo')
                l2 = lines.index('```')
            except:
                print 'blog ' + fname + ' doesn\'t have \
                    correct meta data, skipped!'

            meta = {}
            for line in lines[l1+1:l2]:
                info = line.split(':')
                meta[info[0].strip(' ')] = info[1].strip(' ').strip('"')

            for item in MIN_META_LIST:
                if item in meta:
                    eval('self.' + item + '=' + meta[item])
                else:
                    print 'meta data ' + item + 'lacked, use default value..'

            self.content = lines[l2+1:]
