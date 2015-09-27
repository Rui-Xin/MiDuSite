import MDConfig
import MDEntry
import sys
import importlib


class Generator:
    initialized = False

    def __init__(self, mdconfig):
        if not isinstance(mdconfig, MDConfig.MDConfig):
            print "Invalid config file! Skipped.."
        self.default = mdconfig._default
        self.mdvar = mdconfig.get_mdvar()
        self.initialized = True

    def generate(self):
        pass

    def get_MDEntry(self):
        if 'parser' in self.default:
            module = self.default['paser'].split('.')
        else:
            return MDEntry.MDEntry

        sys.path.insert(0, 'lib/' + self.default['template'] + '/code')
        mod = importlib.import_module(module[0])
        klass = getattr(mod, module[1])
        if issubclass(klass, MDEntry.MDEntry):
            return klass
        else:
            return MDEntry.MDEntry
