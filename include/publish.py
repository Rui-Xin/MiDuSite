import sys
import os
import Generator
import MDConfig

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, 'include')


def publish(section):
    mdconfig_src = MDConfig.MDConfig('source/' + section)
    try:
        template = mdconfig_src._default['template']
    except KeyError:
        print "template not found in " + section + "! Skipped..."
        return
    mdconfig_template = MDConfig.MDConfig('lib/template/' + template)
    mdconfig = mdconfig_template.merge(mdconfig_src)
    mdconfig.addSection(section)
    generator = Generator.Generator(mdconfig)
    generator.generate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        section = './'
    else:
        section = sys.argv[1]

    if not os.path.exists('source/' + section):
        print 'Section ' + section + ' doesn\'t exist!'
        sys.exit(1)

    publish(section)
