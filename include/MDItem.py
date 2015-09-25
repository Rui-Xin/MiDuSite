class MDItem:
    'The object properties reading from .md files'

    def __init__(self, fname):
        with open(fname) as f:
            lines = f.readlines()
            print 'processing ' + fname
            try:
                l1 = lines.index('```MiduSite')
                l2 = lines.index('```')
            except ValueError:
                print 'file ' + fname + ' doesn\'t have \
                    correct meta data, skipped!'

            meta = {}
            for line in lines[l1+1:l2]:
                info = line.split(':')
                meta[info[0].strip(' ')] = info[1].strip(' ').strip('"')

            self.content = lines[l2+1:]
