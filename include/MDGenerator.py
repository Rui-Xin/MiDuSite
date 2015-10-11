import MiduHelper
import MDConfig
import MDEntry
import MDPageTemplates
import MDSnippetTemplates
import MDCallRef
import MDSite
import copy
import math
import re
import os
import shutil
from distutils import dir_util
from collections import OrderedDict


class MDGenerator(object):
    initialized = False
    DEFAULT_HANDLERS = [('GLOBAL', 'generateGlobal'),
                        ('LOCAL', 'generateLocal'),
                        ('PATH', 'generatePath'),
                        ('CALL', 'generateCall'),
                        ('LIST', 'generateList'),
                        ('LISTINFO', 'generateListinfo'),
                        ('SNIPPET', 'generateSnippet'),
                        ('PAGE', 'generatePage'),
                        ('Site', 'generateSite')]

    def __init__(self, mdconfig):
        if not isinstance(mdconfig, MDConfig.MDConfig):
            print "Invalid config file! Skipped.."
        self.default = mdconfig._default
        self.mdvar = mdconfig.get_mdvar()
        self.mdvar._path['src_prefix'] =\
            'source/' + self.default['section'] + '/'
        self.mdvar._path['dst_prefix'] =\
            'published/' + self.default['section'] + '/'
        self.mdvar._path['tmpl_prefix'] =\
            'lib/template/' + self.default['template'] + '/'
        pathlst = {'root': os.path.relpath('./'),
                   'curdir': os.path.relpath('./'),
                   'curpage': '',
                   'pg_tmpl': '',
                   'pg_para': ''}
        self.mdvar.update_path(pathlst)

        self.page_cached = {}
        self.site_cached = {}
        self.entry_cached = {}
        self.handlers = OrderedDict()
        for default_handler in self.DEFAULT_HANDLERS:
            self.addHandler(default_handler[0], default_handler[1])

        self.loaded = {'page': MDPageTemplates.MDPageTemplates(None),
                       'snippet': MDSnippetTemplates.MDSnippetTemplates(None),
                       'code': MDCallRef.MDModuleRef(None)}
        for item in self.loaded:
            self.loaded[item].addFolder(self.mdvar._path['tmpl_prefix'] +
                                        '/' + item)
            src_folder = self.mdvar._path['src_prefix'] + '/' + item
            if os.path.isdir(src_folder):
                self.loaded[item].addFolder(src_folder)

        self.initialized = True

    def generate(self):
        if 'startpage' not in self.default:
            print "startpage not found! Skip generating.."
            return
        matchobj = re.match('([^}]*)', self.default['startpage'])

        dst = os.path.relpath(self.mdvar._path['dst_prefix'] +
                              self.mdvar._path['root'])
        if os.path.exists(dst):
                shutil.rmtree(dst)
        os.mkdir(dst)

        # CSS
        self.copy_directory('css')
        # JS
        self.copy_directory('js')

        if 'pre_process' in self.default:
            to_process = self.default['pre_process'].split(',')
            for call in to_process:
                self.process_callsite(call)

        page = self.generatePage(matchobj)
        print page + ' generated.'
        return page

    def addHandler(self, syntax, handler):
        if syntax not in self.handlers:
            self.handlers.update([(syntax, getattr(self, handler))])

    def generateSite(self, site):
        site_info = MiduHelper.parseVar(site.group(1))['target']
        if site_info not in self.site_cached:
            mdsite = MDSite.MDSite(site_info)
            self.site_cached[site_info] = mdsite.generate()
        return self.site_cached[site_info]

    def generatePage(self, page):
        page_info = MiduHelper.parseVar(page.group(1))
        bkpath = self.mdvar.path_backup()
        self.mdvar._path['pg_tmpl'] = page_info['target']
        self.mdvar._path['pg_para'] = page_info['paras']
        if self.mdvar._listinfo['in_list'] and \
                'dst' not in page_info['paras']:
            rel_path = os.path.relpath(
                self.mdvar._listinfo['list_root'],
                self.mdvar._path['curdir'])
            targ_path = rel_path + '/' + page_info['target']
            page_info['paras']['dst'] = targ_path

        if 'suffix' in page_info['paras']:
            page_info['paras']['dst'] += page_info['paras']['suffix']
        self.mdvar.path_changepage(page_info['paras']['dst'])
        dst_name = self.mdvar._path['curdir'] + '/' +\
            self.mdvar._path['curpage'] + '.html'

        if dst_name in self.page_cached:
            self.mdvar.path_restore(bkpath)
            return dst_name

        MiduHelper.mkdir_p(self.mdvar._path['dst_prefix'] +
                           self.mdvar._path['curdir'])

        with open(self.mdvar._path['dst_prefix'] +
                  dst_name, 'w') as f_w:
            lines = self.loaded['page'].get(page_info['target'])
            self.page_cached[dst_name] = dst_name
            new_lines = self.replace(lines)
            f_w.write(new_lines)
            self.mdvar.path_restore(bkpath)

            return dst_name

        self.mdvar.path_restore(bkpath)

        return ''

    def generateSnippet(self, snippet):
        snippet_tmpl = snippet.group(1)
        lines = self.loaded['snippet'].get(snippet_tmpl)
        return self.replace(lines)

    def generateList(self, lst):
        listcall = MiduHelper.parseVar(lst.group(1))
        if 'dst' not in listcall['paras']:
            print "list " + lst.group(1) + "incompleted! Skipped.."
            return
        snippet = re.match('(.*)', listcall['target'])
        folder = listcall['paras']['dst']
        lst_dir = self.mdvar._path['src_prefix'] + folder
        self.find_entry(lst_dir)

        entries = self.entry_cached[lst_dir][0]
        file_num_map = self.entry_cached[lst_dir][1]
        entries_filtered = self.filter_entries(entries, listcall)
        total_cnt = len(entries_filtered)
        list_lines = []

        listinfo_bk = self.mdvar.listinfo_backup()

        if 'slices' in listcall['paras']:
            if int(self.mdvar._listinfo['cnt']) == 0:
                self.mdvar._listinfo['page_total_cnt'] =\
                    listcall['paras']['slices']
                pages = [self.mdvar._path['curpage'] + '.html']
                total_pages = math.ceil(total_cnt*1.0 /
                                        int(listcall['paras']['slices'])) + 1
                for i in range(2, int(total_pages + 1)):
                    pages.append(self.mdvar._path['curpage'] +
                                 '_' + str(i) + '.html')
                self.mdvar._listinfo['subpage_list'] = pages
        else:
            self.mdvar._listinfo['cnt'] = 0
            self.mdvar._listinfo['page_total_cnt'] = total_cnt

        cnt = int(self.mdvar._listinfo['cnt'])
        for slice_num in range(int(self.mdvar._listinfo['page_total_cnt'])):
            cnt += 1
            self.mdvar._listinfo['cnt'] = str(cnt)
            if cnt > total_cnt:
                self.mdvar._listinfo['cnt'] == '0'
                self.mdvar._listinfo['subpage_list'] = []
                break

            cur_index = entries_filtered.keys()[cnt-1]
            entry = entries_filtered[cur_index]

            self.mdvar._listinfo['list_map'] = file_num_map
            self.mdvar._listinfo['list_root'] = folder
            self.mdvar._listinfo['num'] = str(cur_index)
            self.mdvar._listinfo['page_cnt'] = str(slice_num + 1)
            self.mdvar._listinfo['cnt'] = str(cnt)
            self.mdvar._listinfo['total_cnt'] = str(total_cnt)
            self.mdvar._listinfo['prev_entry'] = \
                MiduHelper.od_prev_entry_meta(entries, cur_index)
            self.mdvar._listinfo['next_entry'] = \
                MiduHelper.od_next_entry_meta(entries, cur_index)
            self.mdvar._listinfo['in_list'] = True

            local_bk = self.mdvar.local_backup()
            entry.processContext()
            self.mdvar.update_local(entry.get_mdlocal())

            list_lines.append(self.generateSnippet(snippet))

            self.mdvar.local_restore(local_bk)

        if cnt < total_cnt:
            idx = self.mdvar._listinfo['subpage_list'].index(
                self.mdvar._path['curpage'] + '.html') + 1
            new_page_name = self.mdvar._listinfo['subpage_list'][idx]
            new_para_dict = copy.deepcopy(self.mdvar._path['pg_para'])
            new_para_dict.update({'dst': new_page_name.replace('.html', ''),
                                  'suffix': ''})
            new_page_para = MiduHelper.generate_parameter(new_para_dict)
            matchobj = re.match('(.*)',
                                self.mdvar._path['pg_tmpl'] +
                                new_page_para)
            self.generatePage(matchobj)

        self.mdvar.listinfo_restore(listinfo_bk)
        return '\n'.join(list_lines)

    def filter_entries(self, entries, listcall):
        if 'filter' in listcall['paras']:
            to_filter = listcall['paras']['filter'].split(':')
            entries_filtered = OrderedDict()
            for entry in entries:
                if to_filter[0] in entries[entry].meta:
                    if type(entries[entry].meta[to_filter[0]]) is list:
                        if to_filter[1] in entries[entry].meta[to_filter[0]]:
                            entries_filtered[entry] = entries[entry]
                    elif entries[entry].meta[to_filter[0]] == to_filter[1]:
                        entries_filtered[entry] = entries[entry]
            return entries_filtered
        else:
            return entries

    def find_entry(self, lst_dir):
        if lst_dir not in self.entry_cached:
            if 'md_suffix' in self.default:
                md_suffix = '.' + self.default['md_suffix']
            else:
                md_suffix = '.md'
            files = filter(lambda x: x.endswith(md_suffix),
                           os.listdir(lst_dir))
            MDEntry = self.get_MDEntry()
            entry_list = []
            file_map = {}
            for f in sorted(files, reverse=True):
                entry = MDEntry(lst_dir + '/' + f, self.mdvar)
                entry_list.append(entry)
                file_map[entry] = f

            if 'mdsort' in self.default:
                sort_fun = self.default['mdsort']
                entry_list = \
                    self.process_callsite(sort_fun,
                                          external=True,
                                          args=[entry_list])

            entries = OrderedDict()
            file_num_map = {}
            i = 1
            for entry in entry_list:
                entries[i] = entry
                file_num_map[file_map[entry]] = i
                i += 1
            self.entry_cached[lst_dir] = [entries, file_num_map]

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
        return self.process_callsite(call)

    def generateGlobal(self, _global):
        varname = _global.group(1)
        if varname in self.mdvar._global:
            return self.mdvar._global[varname]
        else:
            return ''

    def generateLocal(self, _local):
        if not self.mdvar._listinfo['in_list']:
            return 'not found'
        varname = _local.group(1)
        if varname in self.mdvar._local:
            if varname == 'tag' and \
                    type(self.mdvar._local[varname]) is list:
                return ', '.join(self.mdvar._local[varname])
            return self.mdvar._local[varname]
        else:
            return 'not found'

    def generateListinfo(self, _listinfo):
        if not self.mdvar._listinfo['in_list']:
            return 'not_in_list'
        varname = _listinfo.group(1)
        if varname in self.mdvar._listinfo:
            return self.mdvar._listinfo[varname]
        else:
            return 'not found'

    def replace(self, lines):
        for syntax in self.handlers:
            lines = re.sub('\$\{' + syntax + ':([^}]*)\}',
                           self.handlers[syntax],
                           lines,
                           count=0)
        return lines

    def process_callsite(self, call_site, external=False, args=None):

        call_info = MiduHelper.parseVar(call_site)
        file_info = os.path.split(call_info['target'])
        fun_info = call_info['paras']

        fname = file_info[1]
        fun_name = fun_info['name']

        if not external:
            para_list = [self]
        else:
            para_list = []

        if 'arguments' in fun_info:
            para_list.extend(list(fun_info['arguments'].split(',')))
        elif args is not None:
            para_list.extend(args)

        target_module = self.loaded['code'].get(fname)
        func = getattr(target_module, fun_name)
        return func(*para_list)

    def get_MDEntry(self):
        if 'parser' in self.default:
            module = self.default['parser'].split('.')
        else:
            return MDEntry.MDEntry

        mod = self.loaded['code'].get(module[0])
        klass = getattr(mod, module[1])
        if issubclass(klass, MDEntry.MDEntry):
            return klass
        else:
            return MDEntry.MDEntry

    def copy_directory(self, target):
        if os.path.exists(self.mdvar._path['dst_prefix'] +
                          self.mdvar._path['root'] + '/' +
                          target):
            shutil.rmtree(self.mdvar._path['dst_prefix'] +
                          self.mdvar._path['root'] + '/' +
                          target)
        os.mkdir(self.mdvar._path['dst_prefix'] +
                 self.mdvar._path['root'] + '/' +
                 target)

        targs = [self.mdvar._path['tmpl_prefix'] + target,
                 self.mdvar._path['src_prefix'] + target]
        dst = self.mdvar._path['dst_prefix'] +\
            self.mdvar._path['root'] +\
            '/' + target
        for folder in targs:
            if folder in targs:
                if os.path.exists(folder):
                    dir_util.copy_tree(folder, dst)
