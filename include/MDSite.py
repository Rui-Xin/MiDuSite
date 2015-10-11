import MDConfig
import MDGenerator
import MiduHelper


class MDSite:
    def __init__(self, section):
        mdconfig_src = MDConfig.MDConfig('source/' + section)
        try:
            template = mdconfig_src._default['template']
        except KeyError:
            print "template not found in " + section + "! Skipped..."
            return
        mdconfig_template = MDConfig.MDConfig('lib/template/' + template)
        mdconfig = mdconfig_template.merge(mdconfig_src)
        mdconfig.addSection(section)

        if 'generator' in mdconfig._global:
            generator_name = mdconfig._global['generator']
            self.generator = \
                MiduHelper.fun_call('lib/template/' + template + '/code',
                                    generator_name,
                                    generator_name,
                                    [mdconfig])

        else:
            self.generator = MDGenerator.MDGenerator(mdconfig)

    def generate(self):
        return self.generator.generate()
