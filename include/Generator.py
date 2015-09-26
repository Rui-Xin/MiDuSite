import MDConfig
import MDvar


class Generator:
    initialized = False

    def __init__(self, mdconfig):
        if not isinstance(mdconfig, MDconfig):
            print "Invalid config file! Skipped.."
        self.default = mdconfig.default
        self.mdvar = mdconfig.get_mdvar()
        self.initialized = True

    def generate():
        pass
