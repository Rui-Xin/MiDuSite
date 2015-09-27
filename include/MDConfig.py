import ConfigParser
import MDvar
import copy


class MDConfig:
    def __init__(self, directory=''):
        config = ConfigParser.ConfigParser()
        config.read(directory + '/config')
        if config.has_section('default'):
            self._default = dict(config.items('default'))
        else:
            self._default = {}
        if config.has_section('global'):
            self._global = dict(config.items('global'))
        else:
            self._global = {}

    def copy(self):
        return copy.deepcopy(self)

    def merge(self, mdconfig):
        if not isinstance(mdconfig, MDConfig):
            print "File format incorrect, failed to config!"
            return

        new_mdconfig = self.copy()

        new_mdconfig._default.update(mdconfig._default)
        new_mdconfig._global.update(mdconfig._global)

        return new_mdconfig

    def get_mdvar(self):
        return MDvar.MDvar(_global=self._global)

    def addSection(self, section):
        self._default['section'] = section
