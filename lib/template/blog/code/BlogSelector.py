import re
import os


def generate_partition(generator, partition, dst, pagestyle):
    lines = []
    homepage = \
        os.path.relpath(generator.mdvar.path_getroot() + '/' + 'index.html')
    if pagestyle == 'home_page':
        lines.append('<li class=subnav-selected><a href="' +
                     homepage +
                     '">' +
                     'All</a></li>')
    else:
        lines.append('<li>' +
                     '<a href="' +
                     homepage +
                     '">All</a></li>')

    lst_dir = generator.mdvar._path['src_prefix'] + dst
    generator.find_entry(lst_dir)
    entries = generator.entry_cached[lst_dir][0]

    partition_list = []
    for entry in entries:
        if partition in entries[entry].meta:
            merge(partition_list, entries[entry].meta[partition])

    partition_list = sorted(set(partition_list))

    generated = 'generated_' + partition
    page_map = partition + '_page_map'
    if generated not in generator.mdvar._global:
        generator.mdvar._global[generated] = []
        generator.mdvar._global[page_map] = {}
        for part in partition_list:
            generator.mdvar._global[page_map][part] =\
                partition + str(partition_list.index(part) + 1) + '.html'

    for part in partition_list:
        if part not in generator.mdvar._global[generated] and\
                pagestyle == 'home_page':
            new_page = partition + '[dst:' +\
                generator.mdvar.path_getroot() +\
                '/' + partition +\
                str(partition_list.index(part) + 1) +\
                ']'
            generator.mdvar._global[generated].append(part)
            generator.generatePage(re.match('(.*)', new_page))

        pagename = generator.mdvar._global[page_map][part]
        link = os.path.relpath(generator.mdvar.path_getroot() + '/' + pagename)

        if pagestyle == partition + '_page' and \
                part == get_cur_partition(generator, partition):
            lines.append('<li class="subnav-selected">' +
                         '<a href="' +
                         link +
                         '">' +
                         part +
                         '</a></li>')
        else:
            lines.append('<li><a href="' +
                         link +
                         '">' +
                         part +
                         '</a></li>')

    return '\n'.join(lines)


def get_cur_partition(generator, partition):
    cur_part = generator.mdvar._global['generated_' + partition][-1]
    generator.mdvar._path['temp_cur_' + partition] = cur_part
    return cur_part


def merge(partition_list, item):
    if type(item) is list:
        return partition_list.extend(item)
    else:
        return partition_list.append(item)
