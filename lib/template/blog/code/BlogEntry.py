import time
import MDEntry
import markdown
from BeautifulSoup import BeautifulSoup


class BlogEntry(MDEntry.MDEntry):
    'The object of a single blog, reading from .md files'
    meta = {'title': 'Untitled',
            'date': str(time.gmtime),
            'tag': [],
            'content': '',
            'description': ''}

    def __init__(self, fname):
        super(BlogEntry, self).__init__(fname)
        self.meta['origin_description'] =\
            self.meta['content'][:min(500, len(self.meta['content']))]
        self.meta['description'] =\
            markdown.markdown(BeautifulSoup(self.meta['origin_description'])
                              .prettify())
