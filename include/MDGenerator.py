import MiduHelper
import MDConfig
import MDEntry
import sys
import importlib
import re
import os
import shutil
from collections import OrderedDict


class MDGenerator(object):
    initialized = False
    DEFAULT_HANDLERS = [('GLOBAL', 'generateGlobal'),
                        ('LOCAL', 'generateLocal'),
                        ('PATH', 'generatePath'),
                        ('LIST', 'generateList'),
                        ('SNIPPET', 'generateSnippet'),
                        ('PAGE', 'generatePage'),
                        ('CALL', 'generateCall')]

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
                   'curpage': ''}
        self.mdvar.update_path(pathlst)

        self.page_cached = []
        self.handlers = OrderedDict()
        for default_handler in self.DEFAULT_HANDLERS:
            self.addHandler(default_handler[0], default_handler[1])
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

    def addHandler(self, syntax, handler):
        if syntax not in self.handlers:
            self.handlers.update([(syntax, getattr(self, handler))])

    def generatePage(self, page):
        page_info = MiduHelper.parseVar(page.group(1))
        bkpath = self.mdvar.path_backup()
        if self.mdvar._local['in_list'] is True:
            dst_directory = \
                MiduHelper.path_src_to_published(
                    self.mdvar._local['md_directory'])
            rel_path = os.path.relpath(
                dst_directory + '/' + page_info['target'],
                self.dst_prefix + self.mdvar._path['curdir'])
            page_info['paras']['dst'] = rel_path

        self.mdvar.path_changepage(page_info['paras']['dst'])
        fname = self.tmpl_prefix + 'page/' + \
            page_info['target'] + '.html'
        if 'suffix' in page_info['paras']:
            dst_name = self.mdvar._path['curdir'] + '/' +\
                self.mdvar._path['curpage'] + \
                page_info['paras']['suffix'] + \
                '.html'
        else:
            dst_name = self.mdvar._path['curdir'] + '/' +\
                self.mdvar._path['curpage'] + '.html'

        if dst_name in self.page_cached:
            self.mdvar.path_restore(bkpath)
            return dst_name

        MiduHelper.mkdir_p(self.dst_prefix + self.mdvar._path['curdir'])

        with open(fname) as f, open(self.dst_prefix + dst_name, 'w') as f_w:
            lines = f.read()
            new_lines = self.replace(lines)
            f_w.write(new_lines)
            self.mdvar.path_restore(bkpath)
            self.page_cached.append(dst_name)
            return dst_name
        self.mdvar.path_restore(bkpath)

        return ''

    def generateSnippet(self, snippet):
        fname = 'lib/template/' + self.default['template'] + \
            '/snippet/' + snippet.group(1) + '.html'
        with open(fname) as f:
            lines = f.read()
            return self.replace(lines)
        return []

    def generateList(self, lst):
        listcall = MiduHelper.parseVar(lst.group(1))
        if listcall['paras'] == '':
            print "list " + lst.group(1) + "incompleted! Skipped.."
            return
        snippet = re.match('(.*)', listcall['target'])
        folder = listcall['paras']['dst']
        lst_dir = self.src_prefix + self.mdvar._path['root'] + '/' + folder
        files = filter(lambda x: x.endswith('.md'),
                       os.listdir(lst_dir))
        MDEntry = self.get_MDEntry()

        entry_list = []
        file_map = {}
        for f in sorted(files, reverse=True):
            entry = MDEntry(lst_dir + '/' + f, self.mdvar)
            entry_list.append(entry)
            file_map[entry] = f

        if 'mdsort' in self.mdvar._global:
            sort_file = os.path.split(self.mdvar._global['mdsort'])
            directory = self.tmpl_prefix + 'code/' + sort_file[0]
            fname = sort_file[1]
            fun_name = 'sort'
            arguments = [entry_list]
            entry_list = \
                MiduHelper.fun_call(directory, fname, fun_name, arguments)

        entries = OrderedDict()
        file_num_map = {}
        self.mdvar.res_cnt()
        for entry in entry_list:
            entries[self.mdvar._local['cnt']] = entry
            file_num_map[file_map[entry]] = self.mdvar._local['cnt']
            self.mdvar.inc_cnt()
        total_cnt = len(entries)

        list_lines = []
        for entry_num in entries:
            entry = entries[entry_num]
            local_bk = self.mdvar.local_backup()
            listinfo_bk = self.mdvar.listinfo_backup()
            self.mdvar._listinfo['list_map'] = file_num_map
            entry.processContext()
            self.mdvar.update_local(entry.get_mdlocal())
            self.mdvar._local['cnt'] = str(entry_num)
            self.mdvar._local['total_cnt'] = str(total_cnt)
            self.mdvar._local['prev_entry'] = \
                MiduHelper.od_prev_entry_meta(entries, entry_num)
            self.mdvar._local['next_entry'] = \
                MiduHelper.od_next_entry_meta(entries, entry_num)
            self.mdvar._local['in_list'] = True

            list_lines.append(self.generateSnippet(snippet))

            self.mdvar.listinfo_restore(listinfo_bk)
            self.mdvar.local_restore(local_bk)
        return '\n'.join(list_lines)

    def generatePath(self, _path):
        varname = _path.group(1)
        if varname == 'root':
            return self.mdvar.path_getroot()
        if varname in self.mdvar._path:
            return self.mdvar._path[varname]
        else:
            return ''

    def generateCall(self, _call):
        call = _call.group(1)
        call_info = MiduHelper.parseVar(call)
        file_info = os.path.split(call_info['target'])
        fun_info = call_info['paras']

        directory = os.path.relpath(self.tmpl_prefix + 'code/' + file_info[0])
        fname = file_info[1]
        fun_name = fun_info['name']
        para_list = [self]
        if 'arguments' in fun_info:
            para_list.extend(list(fun_info['arguments']))
        return MiduHelper.fun_call(directory, fname, fun_name, para_list)

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
        for syntax in self.handlers:
            lines = re.sub('\$\{' + syntax + ':([^}]*)\}',
                           self.handlers[syntax],
                           lines,
                           count=0)
        return lines

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
