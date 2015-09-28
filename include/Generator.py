import MiduHelper
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
        pathlst = {'root': os.path.relpath('./'),
                   'curdir': os.path.relpath('./'),
                   'curpage': []}
        self.mdvar.update_path(pathlst)
        self.initialized = True

    def generate(self):
        if 'startpage' not in self.default:
            print "startpage not found! Skip generating.."
            return
        matchobj = re.match('([^}]*)', self.default['startpage'])

        dst = os.path.relpath(self.dst_prefix + self.mdvar._path['root'])
        if os.path.exists(dst):
                shutil.rmtree(dst)
        os.mkdir(dst)

        if os.path.exists(self.dst_prefix + self.mdvar._path['root'] + '/css'):
                shutil.rmtree(self.dst_prefix +
                              self.mdvar._path['root'] +
                              '/css')
        shutil.copytree(self.tmpl_prefix + '/css',
                        self.dst_prefix + self.mdvar._path['root'] + '/css')

        print self.generatePage(matchobj) + ' generated.'

    def generatePage(self, page):
        page_info = MiduHelper.parseVar(page.group(1))
        bkpath = self.mdvar.path_backup()
        self.mdvar.path_changeindex(page_info['paras'][0])
        fname = self.tmpl_prefix + 'page/' + \
            page_info['target'] + '.html'
        if len(page_info['paras']) > 1:
            dst_name = self.mdvar._path['curdir'] + '/' +\
                self.mdvar._path['curpage'] + \
                page_info['paras'][1] + \
                '.html'
        else:
            dst_name = self.mdvar._path['curdir'] + '/' +\
                self.mdvar._path['curpage'] + '.html'
        MiduHelper.mkdir_p(self.dst_prefix + self.mdvar._path['curdir'])

        with open(fname) as f, open(self.dst_prefix + dst_name, 'w') as f_w:
            lines = f.readlines()
            new_lines = self.replace(lines)
            f_w.write(''.join(new_lines))
            self.mdvar.path_restore(bkpath)
            return dst_name
        self.mdvar.path_restore(bkpath)
        return ''

    def generateSnippet(self, snippet):
        fname = 'lib/template/' + self.default['template'] + \
            '/snippet/' + snippet.group(1) + '.html'
        with open(fname) as f:
            lines = f.readlines()
            return self.replace(lines)
        return []

    def generateList(self, lst):
        listcall = MiduHelper.parseVar(lst.group(1))
        if listcall['paras'] == '':
            print "list " + lst.group(1) + "incompleted! Skipped.."
            return
        snippet = re.match('(.*)', listcall['target'])
        folder = listcall['paras'][0]
        lst_dir = self.src_prefix + self.mdvar._path['root'] + '/' + folder
        files = filter(lambda x: '.md' in x,
                       os.listdir(lst_dir))
        MDEntry = self.get_MDEntry()

        list_lines = []
        self.mdvar.res_cnt()
        for f in sorted(files, reverse=True):
            entry = MDEntry(lst_dir + '/' + f)
            self.mdvar.update_local(entry.get_mdvar()._local)
            list_lines.append(self.generateSnippet(snippet))
            self.mdvar.empty_local()
            self.mdvar.inc_cnt()
        return '\n'.join(list_lines)

    def generatePath(self, _path):
        varname = _path.group(1)
        if varname == 'root':
            return self.mdvar.path_getroot()
        if varname in self.mdvar._path:
            return self.mdvar._path[varname]
        else:
            return ''

    def generateGlobal(self, _global):
        varname = _global.group(1)
        if varname in self.mdvar._global:
            return self.mdvar._global[varname]
        else:
            return ''

    def generateLocal(self, _local):
        varname = _local.group(1)
        if varname == 'cnt':
            return str(self.mdvar._localcnt)

        if varname in self.mdvar._local:
            return self.mdvar._local[varname]
        else:
            return 'not found'

    def replace(self, lines):
        new_lines = re.sub('\$\{GLOBAL:([^}]*)\}',
                           self.generateGlobal, ''.join(lines), count=0)
        new_lines = re.sub('\$\{LOCAL:([^}]*)\}',
                           self.generateLocal, new_lines, count=0)
        new_lines = re.sub('\$\{PATH:([^}]*)\}',
                           self.generatePath, new_lines, count=0)
        new_lines = re.sub('\$\{LIST:([^}]*)\}',
                           self.generateList, new_lines, count=0)
        new_lines = re.sub('\$\{SNIPPET:([^}]*)\}',
                           self.generateSnippet, new_lines, count=0)
        new_lines = re.sub('\$\{PAGE:([^}]*)\}',
                           self.generatePage, new_lines, count=0)
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
