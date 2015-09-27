class MDvar:
    def __init__(self, _local={}, _global={}):
        self._local = _local
        self._global = _global

    def update_global(self, _global):
        if isinstance(_global, dict):
            self._global.update(_global)

    def update_local(self, _local):
        if isinstance(_local, dict):
            self._local = _local

    def update(self, _local, _global):
        self.update_local(_local)
        self.update_global(_global)
