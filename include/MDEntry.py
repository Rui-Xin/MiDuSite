import markdown
import re
import os
import shutil
import MiduHelper
import copy
import urllib2


class MDEntry(object):
    'The object properties reading from .md files'

    DEFAULT_HANDLERS = {'img': 'img_generator',
                        'latex': 'latex_generator'}

    def __init__(self, fname, mdvar):
        self.mdvar = mdvar
        self.meta = {}
        file_info = os.path.split(fname)
        self.meta['md_filename'] = file_info[1]
        self.meta['md_directory'] = file_info[0]

        self.img_count = 1
        self.latex_count = 1

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
                self.meta[info[0].strip(' ')] = ':'.join(val).strip('\n')

            self.meta['origin_content'] = ''.join(lines[l2+1:])
            self.meta['content'] = \
                markdown.markdown(
                    self.meta['origin_content'])

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
        split = list(os.path.split(img_file))
        new_name = str(self.mdvar._listinfo['num']) + '_' + str(self.img_count)
        split[1] = re.sub('.*(\.[^\.]*)', new_name + r'\1', split[1])
        new_img_file = os.path.join(*split)

        src = self.mdvar._path['src_prefix'] +\
            self.mdvar._listinfo['list_root'] +\
            '/' + img_file
        dst = self.mdvar._path['dst_prefix'] +\
            self.mdvar._listinfo['list_root'] +\
            '/' + new_img_file

        dst_directory = os.path.split(dst)[0]
        if not os.path.exists(dst_directory):
            MiduHelper.mkdir_p(dst_directory)
        shutil.copyfile(src, dst)
        IMG_HTML.insert(1, new_img_file)

        self.img_count += 1

        return ''.join(IMG_HTML)

    def latex_generator(self, matchobj):
        URL_prefix =\
            'https://latex.codecogs.com/png.download?%5Cdpi%7B150%7D%20'
        IMG_HTML = ['<p><img src="', '"></p>']
        latex_f = matchobj.group(1).strip()

        new_name = str(self.mdvar._listinfo['num']) + '_' +\
            str(self.latex_count) + '.png'

        dst = self.mdvar._path['dst_prefix'] +\
            self.mdvar._listinfo['list_root'] +\
            '/css/' + new_name

        dst_directory = os.path.split(dst)[0]
        if not os.path.exists(dst_directory):
            MiduHelper.mkdir_p(dst_directory)
            shutil.copyfile('include/latexnotfound.png',
                            dst_directory + '/latexnotfound.png')

        if not latex_f.startswith('$') and not latex_f.endswith('$'):
            print 'latex fomula ' + latex_f + 'format incorrect'
            return ''
        latex_f = urllib2.quote(latex_f[1:-1])
        try:
            png = urllib2.urlopen(URL_prefix + latex_f).read()
        except urllib2.URLError:
            return IMG_HTML[0] + 'css/latexnotfound.png' + IMG_HTML[1]

        if 'Error: Invalid Equation' in png:
            print 'latex fomula ' + latex_f + 'format incorrect'
            return ''

        with open(dst, 'w') as f:
            f.write(png)

        IMG_HTML.insert(1, 'css/' + new_name)
        self.latex_count += 1

        return ''.join(IMG_HTML)

    def get_mdlocal(self):
        return copy.deepcopy(self.meta)

    def post_process(self):
        pass
