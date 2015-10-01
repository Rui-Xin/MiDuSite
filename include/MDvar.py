import os
import copy


class MDvar:

    DEFAULT_LOCAL = {'cnt': 1,
                     'total_cnt': 0,
                     'prev_entry': None,
                     'next_entry': None,
                     'md_filename': '',
                     'md_directory': '',
                     'in_list': False
                     }

    DEFAULT_LISTINFO = {'list_map': {},
                        'list_root': None}

    def __init__(self, _local=DEFAULT_LOCAL, _global={}):
        self._local = _local
        self._global = _global
        self._path = {'root': os.path.relpath(os.path.curdir),
                      'curdir': os.path.relpath(os.path.curdir),
                      'curpage': '',
                      'from_page': ''}
        self._listinfo = self.DEFAULT_LISTINFO

    def update_global(self, _global):
        if isinstance(_global, dict):
            self._global.update(_global)

    def update_local(self, _local):
        if isinstance(_local, dict):
            self._local = _local

    def update_path(self, _path):
        if isinstance(_path, dict):
            self._path.update(_path)

    def path_changepage(self, _page):
        _tochange = os.path.split(_page)
        self._path['from_page'] = \
            os.path.relpath('.', _tochange[0]) + '/' +\
            self._path['curpage'] + '.html'
        self.path_cd(_tochange[0])
        self._path['curpage'] = _tochange[1]

    def path_backup(self):
        return copy.deepcopy(self._path)

    def path_restore(self, backup):
        if type(backup) is dict and \
                'root' in backup and \
                'curdir' in backup and \
                'curpage' in backup and \
                'from_page' in backup:
            self._path = backup

    def path_cd(self, _directory):
        new_path = os.path.join(self._path['curdir'], _directory)
        self._path['curdir'] = os.path.relpath(new_path)

    def path_getupper(self):
        new_path = os.path.join(self._path['curdir'], '..')
        return os.path.relpath(new_path)

    def path_getroot(self):
        return os.path.relpath(self._path['root'], self._path['curdir'])

    def local_backup(self):
        return copy.deepcopy(self._local)

    def local_restore(self, backup):
        if type(backup) is dict:
            self._local = backup

    def listinfo_backup(self):
        return copy.deepcopy(self._listinfo)

    def listinfo_restore(self, backup):
        if type(backup) is dict:
            self._listinfo = backup

    def inc_cnt(self):
        self._local['cnt'] += 1

    def res_cnt(self):
        self._local['cnt'] = 1

    def update(self, _local, _global):
        self.update_local(_local)
        self.update_global(_global)
