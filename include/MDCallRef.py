import os
import sys
import importlib


class MDModuleRef:
    def __init__(self, init_folder):
        self.modules = {}
        if init_folder is not None:
            self.addFolder(init_folder)

    def addFolder(self, folder):
        files = os.listdir(folder)
        for f in files:
            if not f.endswith('.py'):
                continue
            self.addModule(folder + '/' + f)

    def addModule(self, f):
        folder = os.path.abspath(os.path.split(f)[0])
        fname = os.path.split(f)[1]
        module_name = fname.replace('.py', '')

        remove_path = True
        if folder in sys.path:
            remove_path = False
        else:
            sys.path.insert(0, folder)
        target_module = importlib.import_module(module_name, folder)
        if remove_path:
            sys.path.remove(folder)

        self.addRef(module_name, target_module)

    def addRef(self, module_name, target_module):
        self.modules[module_name] = target_module

    def get(self, mod):
        return self.modules[mod]
