import sys
import os
import MDSite
import shutil

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, 'include')


def publish(section):
    site = MDSite.MDSite(section)
    site.generate()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        section = './'
    else:
        section = sys.argv[1]

    if not os.path.exists('source/' + section):
        print 'Section ' + section + ' doesn\'t exist!'
        sys.exit(1)

    if not section == './' and \
            not section == '' and \
            not section == '.':
        if os.path.exists('published/' + section):
            shutil.rmtree('published/' + section)
        os.mkdir('published/' + section)

    publish(section)
