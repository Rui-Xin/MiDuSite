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

    def __init__(self, fname, mdvar):
        super(BlogEntry, self).__init__(fname, mdvar)
        self.addHandler('mdlink', self.mdlink_handler)

    def mdlink_handler(self, matchobj):
        mdfile = matchobj.group(1)
        number = self.mdvar._listinfo['list_map'][mdfile]
        return 'blog' + str(number) + '.html'

    def post_process(self):
        reduc_content = BeautifulSoup(self.meta['content'])
        for tag in ['embed', 'img', 'a']:
            for match in reduc_content.findAll(tag):
                match.replaceWithChildren()

        html = unicode(reduc_content.prettify(), 'utf-8')
        ori_description =\
            html[:min(300, len(reduc_content.prettify()))].encode('utf-8')
        self.meta['description'] =\
            BeautifulSoup(ori_description).prettify()
