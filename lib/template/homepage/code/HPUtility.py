import os
import re
import sys
import shutil


def sites(generator):
    lines = []
    for section in generator.mdvar._global['sections'].split(','):
        dst = section.replace(' ', '')

        if not os.path.exists('source/' + dst):
            print 'Section ' + dst + ' doesn\'t exist!'
            sys.exit(1)

        if os.path.exists('published/' + dst):
            shutil.rmtree('published/' + dst)
        os.mkdir('published/' + dst)

        matchboj = re.match('(.*)', dst)

        site_link = os.path.relpath(dst +
                                    '/' +
                                    generator.generateSite(matchboj))
        lines.append('<a href="' +
                     site_link +
                     '" class="pure-button pure-button-primary">' +
                     section +
                     '</a>')

    return '\n'.join(lines)
