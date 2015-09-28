import time
import MDEntry


class BlogEntry(MDEntry.MDEntry):
    'The object of a single blog, reading from .md files'
    meta = {'title': 'Untitled',
            'date': str(time.gmtime),
            'tag': [],
            'content': '',
            'description': ''}

    def __init__(self, fname):
        super(BlogEntry, self).__init__(fname)
        self.meta['description'] =\
            self.meta['content'][:min(1000, len(self.meta['content']))]
