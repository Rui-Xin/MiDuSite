import time
import MDEntry
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

        reduc_content = BeautifulSoup(self.meta['content'])
        for tag in ['embed', 'img', 'a']:
            for match in reduc_content.findAll(tag):
                match.replaceWithChildren()

        html = unicode(reduc_content.prettify(), 'utf-8')
        ori_description =\
            html[:min(300, len(reduc_content.prettify()))].encode('utf-8')
        self.meta['description'] =\
            BeautifulSoup(ori_description).prettify()
