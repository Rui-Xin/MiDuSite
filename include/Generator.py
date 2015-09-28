import MDConfig
import MDEntry
import sys
import importlib
import re


class Generator:
    initialized = False

    def __init__(self, mdconfig):
        if not isinstance(mdconfig, MDConfig.MDConfig):
            print "Invalid config file! Skipped.."
        self.default = mdconfig._default
        self.mdvar = mdconfig.get_mdvar()
        self.initialized = True

    def generate(self):
        if 'startpage' not in self.default:
            print "startpage not found! Skip generating.."
            return
        matchobj = re.match('([^}]*)', self.default['startpage'])
        print self.generatePage(matchobj)

    def generatePage(self, page):
        fname = 'lib/template/' + self.default['template'] + \
            '/page/' + page.group(1) + '.html'
        with open(fname) as f:
            lines = f.readlines()
            return self.replace(lines)
        return ''

    def generateSnippet(self, snippet):
        fname = 'lib/template/' + self.default['template'] + \
            '/snippet/' + snippet.group(1) + '.html'
        with open(fname) as f:
            lines = f.readlines()
            return self.replace(lines)
        return []

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
            return ''

    def replace(self, lines):
        new_lines = re.sub('\$\{PAGE:([^}]*)\}',
                           self.generatePage, ''.join(lines), count=0)
        new_lines = re.sub('\$\{SNIPPET:([^}]*)\}',
                           self.generateSnippet, new_lines, count=0)
        new_lines = re.sub('\$\{GLOBAL:([^}]*)\}',
                           self.generateGlobal, new_lines, count=0)
        new_lines = re.sub('\$\{LOCAL:([^}]*)\}',
                           self.generateLocal, new_lines, count=0)
        return new_lines

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
