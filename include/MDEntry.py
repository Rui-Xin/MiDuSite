import markdown
import re
import os
import shutil
import MiduHelper
import copy


class MDEntry(object):
    'The object properties reading from .md files'

#    DEFAULT_HANDLERS = {'img': 'img_generator',
#                        'latex': 'latex_generator'}
    DEFAULT_HANDLERS = {'img': 'img_generator'}

    def __init__(self, fname, mdvar):
        self.mdvar = mdvar

        self.meta = {}
        file_info = os.path.split(fname)
        self.meta['md_filename'] = file_info[1]
        self.meta['md_directory'] = file_info[0]

        self.handlers = {}
        for syntax in self.DEFAULT_HANDLERS:
            self.addHandler(syntax,
                            getattr(self, self.DEFAULT_HANDLERS[syntax]))

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
                val = [x.strip(' ').strip('"') for x in info[1:]]
                self.meta[info[0].strip(' ')] = ':'.join(val)

            self.meta['origin_content'] = ''.join(lines[l2+1:])
            self.meta['content'] = \
                markdown.markdown(self.meta['origin_content'])

    def processContext(self):
        context = self.meta['content']
        for syntax in self.handlers:
            context = re.sub('{\%\ ' + syntax + '\ (.*)\ \%}',
                             self.handlers[syntax],
                             context,
                             count=0)
        self.meta['content'] = context
        self.post_process()

    def addHandler(self, syntax, handler):
        self.handlers[syntax] = handler

    def img_generator(self, matchobj):
        IMG_HTML = ['<p><img src="', '"></p>']
        img_file = matchobj.group(1)
        src = self.meta['md_directory'] + '/' + img_file
        dst = MiduHelper.path_src_to_published(src)

        dst_directory = os.path.split(dst)[0]
        if not os.path.exists(dst_directory):
            MiduHelper.mkdir_p(dst_directory)
        shutil.copyfile(src, dst)
        IMG_HTML.insert(1, img_file)

        return ''.join(IMG_HTML)

    def latex_generator(self, matchobj):
        IMG_HTML = ['<p><img src="', '"></p>']
        latex_f = matchobj.group(1).strip()
        if not f.startswith('$') and not f.endswith('$'):
            return latex_f
        //TODO
        else:

    def get_mdlocal(self):
        return copy.deepcopy(self.meta)

    def post_process(self):
        pass
