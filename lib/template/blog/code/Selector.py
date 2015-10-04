import re
import os


def generateTag(generator, dst, pagestyle):
    lines = []
    homepage = \
        os.path.relpath(generator.mdvar.path_getroot() + '/' + 'index.html')
    if pagestyle == 'homepage':
        lines.append('<li class="pure-menu-item"><a href="' +
                     homepage +
                     '" class="pure-menu-link pure-menu-selected"' +
                     ' style="color:rgb(118, 150, 172)">' +
                     'All</a></li>')
    else:
        lines.append('<li class="pure-menu-item">' +
                     '<a href="' +
                     homepage +
                     '" class="pure-menu-link"">All</a></li>')

    lst_dir = generator.mdvar._path['src_prefix'] + dst
    generator.find_entry(lst_dir)
    entries = generator.entry_cached[lst_dir][0]

    tag_list = []
    for entry in entries:
        tag_list.append(entries[entry].meta['tag'])

    tag_list = sorted(set(tag_list))

    if 'generated_tag' not in generator.mdvar._global:
        generator.mdvar._global['generated_tag'] = []
        generator.mdvar._global['tag_page_map'] = {}
        for tag in tag_list:
            generator.mdvar._global['tag_page_map'][tag] =\
                'tag' + str(tag_list.index(tag) + 1) + '.html'

    for tag in tag_list:
        if tag not in generator.mdvar._global['generated_tag'] and\
                pagestyle == 'homepage':
            new_page = 'tag[dst:' +\
                generator.mdvar.path_getroot() +\
                '/tag' +\
                str(tag_list.index(tag) + 1) +\
                ']'
            generator.mdvar._global['generated_tag'].append(tag)
            generator.generatePage(re.match('(.*)', new_page))

        pagename = generator.mdvar._global['tag_page_map'][tag]
        link = os.path.relpath(generator.mdvar.path_getroot() + '/' + pagename)

        if pagestyle == 'tag_page' and tag == get_cur_tag(generator):
            lines.append('<li class="pure-menu-item pure-menu-selected">' +
                         '<a href="' +
                         link +
                         '" class="pure-menu-link"' +
                         ' style="color:rgb(118, 150, 172)">' +
                         tag +
                         '</a></li>')
        else:
            lines.append('<li class="pure-menu-item"><a href="' +
                         link +
                         '" class="pure-menu-link">' +
                         tag +
                         '</a></li>')

    return '\n'.join(lines)


def get_cur_tag(generator):
    return generator.mdvar._global['generated_tag'][-1]
