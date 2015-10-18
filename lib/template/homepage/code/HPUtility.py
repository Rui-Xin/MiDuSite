import os
import re
import sys
import shutil

NAV='''
<div class="custom-menu-wrapper">
    <div class="pure-menu custom-menu custom-menu-top">
        <a href="#" class="pure-menu-heading custom-menu-brand">Brand</a>
        <a href="#" class="custom-menu-toggle" id="toggle"><s class="bar"></s><s class="bar"></s></a>
    </div>
    <div class="pure-menu pure-menu-horizontal pure-menu-scrollable custom-menu custom-menu-bottom custom-menu-tucked" id="tuckedMenu">
        <div class="custom-menu-screen"></div>
        <ul class="pure-menu-list">
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Home</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">About</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Contact</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Blog</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">GitHub</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Twitter</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Apple</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Google</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Wang</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">Yahoo</a></li>
            <li class="pure-menu-item"><a href="#" class="pure-menu-link">W3C</a></li>
        </ul>
    </div>
</div>
'''

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
                                    generator.generateSite(matchboj, NAV))
        lines.append('<a href="' +
                     site_link +
                     '" class="pure-button pure-button-primary">' +
                     section +
                     '</a>')

    return '\n'.join(lines)
