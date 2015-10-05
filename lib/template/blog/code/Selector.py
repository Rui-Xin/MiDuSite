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
    cur_tag = generator.mdvar._global['generated_tag'][-1]
    generator.mdvar._path['temp_cur_tag'] = cur_tag
    return cur_tag


def generateYear(generator, dst, pagestyle):
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

    year_list = []
    for entry in entries:
        year_list.append(entries[entry].meta['year'])

    year_list = sorted(set(year_list),
                       reverse=True,
                       key=lambda x: re.findall('\d+', x))

    if 'generated_year' not in generator.mdvar._global:
        generator.mdvar._global['generated_year'] = []
        generator.mdvar._global['year_page_map'] = {}
        for year in year_list:
            generator.mdvar._global['year_page_map'][year] =\
                'year' + str(year_list.index(year) + 1) + '.html'

    for year in year_list:
        if year not in generator.mdvar._global['generated_year'] and\
                pagestyle == 'homepage':
            new_page = 'year[dst:' +\
                generator.mdvar.path_getroot() +\
                '/year' +\
                str(year_list.index(year) + 1) +\
                ']'
            generator.mdvar._global['generated_year'].append(year)
            generator.generatePage(re.match('(.*)', new_page))

        pagename = generator.mdvar._global['year_page_map'][year]
        link = os.path.relpath(generator.mdvar.path_getroot() + '/' + pagename)

        if pagestyle == 'year_page' and year == get_cur_year(generator):
            lines.append('<li class="pure-menu-item pure-menu-selected">' +
                         '<a href="' +
                         link +
                         '" class="pure-menu-link"' +
                         ' style="color:rgb(118, 150, 172)">' +
                         year +
                         '</a></li>')
        else:
            lines.append('<li class="pure-menu-item"><a href="' +
                         link +
                         '" class="pure-menu-link">' +
                         year +
                         '</a></li>')

    return '\n'.join(lines)


def get_cur_year(generator):
    cur_year = generator.mdvar._global['generated_year'][-1]
    generator.mdvar._path['temp_cur_year'] = cur_year
    return cur_year
