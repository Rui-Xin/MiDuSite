import os
import copy


class MDvar:
    def __init__(self, _local={}, _global={}):
        self._local = _local
        self._global = _global
        self._path = {'root': os.path.relpath(os.path.curdir),
                      'curdir': os.path.relpath(os.path.curdir),
                      'curpage': []}

    def update_global(self, _global):
        if isinstance(_global, dict):
            self._global.update(_global)

    def update_local(self, _local):
        if isinstance(_local, dict):
            self._local = _local

    def update_path(self, _path):
        if isinstance(_path, dict):
            self._path.update(_path)

    def path_changeindex(self, _index):
        _tochange = os.path.split(_index)
        self.path_cd(_tochange[0])
        self._path['curpage'] = _tochange[1]

    def path_backup(self):
        return copy.deepcopy(self._path)

    def path_restore(self, backup):
        if type(backup) is dict and \
                'root' in backup and \
                'curdir' in backup and \
                'curpage' in backup:
            self._path = backup

    def path_cd(self, _directory):
        new_path = os.path.join(self._path['curdir'], _directory)
        self._path['curdir'] = os.path.relpath(new_path)

    def path_getupper(self):
        new_path = os.path.join(self._path['curdir'], '..')
        return os.path.relpath(new_path)

    def path_getroot(self):
        return os.path.relpath(self._path['root'], self._path['curdir'])

    def empty_local(self):
        self.update_local({})

    def update(self, _local, _global):
        self.update_local(_local)
        self.update_global(_global)
