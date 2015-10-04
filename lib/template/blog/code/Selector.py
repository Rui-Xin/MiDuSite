import re


def generateTag(generator, dst):
    lines = []

    lst_dir = generator.mdvar._path['src_prefix'] + dst
    generator.find_entry(lst_dir)
    entries = generator.entry_cached[lst_dir][0]

    tag_list = []
    for entry in entries:
        tag_list.append(entries[entry].meta['tag'])

    tag_list = sorted(set(tag_list))
    if 'generated_tag' not in generator.mdvar._global:
        generator.mdvar._global['generated_tag'] = []
    for tag in tag_list:
        if tag not in generator.mdvar._global['generated_tag']:
            new_page = 'filter[dst:filter_tag' +\
                str(tag_list.index(tag) + 1) +\
                ']'
            page = generator.generatePage(re.match('(.*)', new_page))
            generator.mdvar._global['generated_tag'].append(tag)

        lines.append('<p>' +
                     tag +
                     '</p>')

    return '\n'.join(lines)


def get_cur_tag(generator):
    return generator.mdvar._global['generated_tag'][-1]
