import time
import MDEntry

MIN_META_LIST = ['title', 'date', 'tag']


class BlogEntry():
    'The object of a single blog, reading from .md files'
    title = 'Untitled'
    date = time.gmtime()
    tag = []
    content = []
    description = []

    def __init__(self, fname):
        super(MDEntry, self).__init__(fname)
        self.description = self.content[:2]
