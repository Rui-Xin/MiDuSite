import os
import copy


class MDPageTemplates:
    def __init__(self, init_folder):
        self.templates = {}
        if init_folder is not None:
            self.addFolder(init_folder)

    def addFolder(self, folder):
        files = os.listdir(folder)
        for f in files:
            if not f.endswith('.html'):
                continue
            self.addFile(folder + '/' + f)

    def addFile(self, f):
        fname = os.path.split(f)[1]
        temp_name = fname.replace('.html', '')
        self.addTemplate(temp_name, f)

    def addTemplate(self, templatename, fname):
        with open(fname) as f:
            self.templates[templatename] = '\n'.join(f.readlines())

    def setContent(self, templatename, content):
        self.templates[templatename] = content

    def get(self, tmpl):
        if tmpl not in self.templates:
            return ''
        return copy.deepcopy(self.templates[tmpl])
