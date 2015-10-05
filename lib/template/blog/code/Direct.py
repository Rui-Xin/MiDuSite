import math
import re
from collections import OrderedDict


def page_direct(generator, dst, slices, _filter, _value):
    lines = ['<div class="footer">',
             '<div class="pure-menu">',
             '<ul class="pure-menu-list">']

    lst_dir = generator.mdvar._path['src_prefix'] + dst
    generator.find_entry(lst_dir)
    entries = generator.entry_cached[lst_dir][0]
    filtered_entries = filter_entries(entries, _filter, _value)

    total = len(filtered_entries)
    slices = int(slices)
    total_pages = int(math.ceil(total * 1.0 / slices))

    cnt = generator.mdvar._listinfo['cnt']
    if cnt == 0:
        page_num = 1
    else:
        page_num = int(math.ceil(int(cnt) * 1.0 / slices)) + 1

    pagename = generator.mdvar._path['curpage']

    if page_num > 1:
        if pagename.endswith('_' + str(page_num)):
            pagename = re.sub('_' + str(page_num) + '$', '', pagename)

        if page_num > 2:
            pagename += '_' + str(page_num - 1)

        prv_line = '<li class="pure-menu-item"><a href="' +\
            pagename +\
            '.html"> Previous Page' +\
            '</a></li>'
        lines.append(prv_line)

    pagename = generator.mdvar._path['curpage']
    if page_num < total_pages:
        if pagename.endswith('_' + str(page_num)):
            pagename = re.sub('_' + str(page_num) + '$', '', pagename)

        pagename += '_' + str(page_num + 1)

        nxt_line = '<li class="pure-menu-item"><a href="' +\
            pagename +\
            '.html"> Next Page' +\
            '</a></li>'
        lines.append(nxt_line)

    lines.extend(['</ul>', '</div>', '</div>'])
    return '\n'.join(lines)


def blog_direct(generator):
    lines = ['<div class="footer">',
             '<div class="pure-menu">',
             '<ul class="pure-menu-list">']

    if not generator.mdvar._listinfo['prev_entry'] is None:
        prv_title = generator.mdvar._listinfo['prev_entry']['title']
        num = generator.mdvar._listinfo['num']
        prv_line = '<li class="pure-menu-item"><a href="blog' +\
            str(int(num)-1) +\
            '.html"> Previous:' +\
            prv_title + \
            '</a></li>'
        lines.append(prv_line)

    if not generator.mdvar._listinfo['next_entry'] is None:
        nxt_title = generator.mdvar._listinfo['next_entry']['title']
        num = generator.mdvar._listinfo['num']
        nxt_line = '<li class="pure-menu-item"><a href="blog' +\
            str(int(num)+1) +\
            '.html"> Next:' +\
            nxt_title + \
            '</a></li>'
        lines.append(nxt_line)

    lines.extend(['</ul>', '</div>', '</div>'])
    return '\n'.join(lines)


def filter_entries(entries, _filter, _value):
    if _filter == 'all':
        filtered_entries = entries
    else:
        filtered_entries = OrderedDict()
        for entry in entries:
            if entries[entry].meta[_filter] == _value:
                filtered_entries[entry] = entries[entry]
    return filtered_entries
