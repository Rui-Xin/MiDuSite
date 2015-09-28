import MDConfig
import MDEntry
import sys
import importlib
import re
import os
import shutil


class Generator:
    initialized = False

    def __init__(self, mdconfig):
        if not isinstance(mdconfig, MDConfig.MDConfig):
            print "Invalid config file! Skipped.."
        self.default = mdconfig._default
        self.mdvar = mdconfig.get_mdvar()
        self.src_prefix = 'source/' + self.default['section'] + '/'
        self.dst_prefix = 'published/' + self.default['section'] + '/'
        self.tmpl_prefix = 'lib/template/' + self.default['template'] + '/'
        self.initialized = True

    def generate(self):
        if 'startpage' not in self.default:
            print "startpage not found! Skip generating.."
            return
        matchobj = re.match('([^}]*)', self.default['startpage'])

        if os.path.exists(self.dst_prefix + 'css'):
                shutil.rmtree(self.dst_prefix)
        shutil.copytree(self.tmpl_prefix + 'css', self.dst_prefix + 'css')

        print self.generatePage(matchobj) + ' generated.'

    def generatePage(self, page):
        pagename = re.search('[^\/]*$', page.group(1)).group(0)
        fname = self.tmpl_prefix + 'page/' + page.group(1) + '.html'
        dst_name = self.dst_prefix + pagename + '.html'
        with open(fname) as f, open(dst_name, 'w') as f_w:
            lines = f.readlines()
            new_lines = self.replace(lines)
            f_w.write(''.join(new_lines))
            return dst_name
        return ''

    def generateSnippet(self, snippet):
        fname = 'lib/template/' + self.default['template'] + \
            '/snippet/' + snippet.group(1) + '.html'
        with open(fname) as f:
            lines = f.readlines()
            return self.replace(lines)
        return []

    def generateList(self, lst):
        listcall = lst.group(1)
        target = re.match('([^\[]*)\[([^\]]*)\]', listcall).groups()
        if len(target) < 2:
            print "list " + listcall + "incompleted! Skipped.."
            return
        snippet = re.match('(.*)', target[0])
        folder = target[1]
        files = filter(lambda x: '.md' in x,
                       os.listdir(self.src_prefix + folder))
        MDEntry = self.get_MDEntry()

        list_lines = []
        for f in files:
            entry = MDEntry(self.src_prefix + folder + '/' + f)
            self.mdvar.update_local(entry.get_mdvar()._local)
            list_lines.append(self.generateSnippet(snippet))
            self.mdvar.empty_local()
        return '\n'.join(list_lines)

    def generateGlobal(self, _global):
        varname = _global.group(1)
        if varname in self.mdvar._global:
            return self.mdvar._global[varname]
        else:
            return ''

    def generateLocal(self, _local):
        varname = _local.group(1)
        if varname in self.mdvar._local:
            return self.mdvar._local[varname]
        else:
            return 'not found'

    def replace(self, lines):
        new_lines = re.sub('\$\{PAGE:([^}]*)\}',
                           self.generatePage, ''.join(lines), count=0)
        new_lines = re.sub('\$\{SNIPPET:([^}]*)\}',
                           self.generateSnippet, new_lines, count=0)
        new_lines = re.sub('\$\{GLOBAL:([^}]*)\}',
                           self.generateGlobal, new_lines, count=0)
        new_lines = re.sub('\$\{LOCAL:([^}]*)\}',
                           self.generateLocal, new_lines, count=0)
        new_lines = re.sub('\$\{LIST:([^}]*)\}',
                           self.generateList, new_lines, count=0)
        return new_lines

    def get_MDEntry(self):
        if 'parser' in self.default:
            module = self.default['parser'].split('.')
        else:
            return MDEntry.MDEntry

        sys.path.insert(0, 'lib/template/'
                        + self.default['template'] + '/code')
        mod = importlib.import_module(module[0])
        klass = getattr(mod, module[1])
        if issubclass(klass, MDEntry.MDEntry):
            return klass
        else:
            return MDEntry.MDEntry
