import ConfigParser


class MDConfig:
    def __init__(self, filename):
        config = ConfigParser.ConfigParser()
        try:
            self._default = dict(config.items('default'))
            self._global = dict(config.items('global'))
        except ConfigParser.NoSectionError:
            print "Config file " + filename + " format error!"
            raise
