import os
import re
import glob
import copy
import shutil
import MiduHelper
import MDEntry


def copy_files(generator):
    src_f = generator.mdvar._path['src_prefix']
    dst_f = generator.mdvar._path['dst_prefix']

    if os.path.exists(src_f):
        for f in glob.glob(src_f + '*.jpg'):
            shutil.copy2(f, dst_f)


COVER='''
<div class="container">
        <h1><a class="" href="${PATH:root}/index.html">${GLOBAL:aboutmename}</a></h1>
        <p>${GLOBAL:desc}</p>
</div>
<div class="subnav container">
<ul>
        to_be_replace
</ul>
</div>
'''

def generate_cover(generator):
    if 'pages' not in generator.mdvar._global:
        return

    pages = generator.mdvar._global['pages'].split(',')
    page_cached = {}
    entries = {}
    for page in pages:
        call = MiduHelper.parseVar(page)

        entry = get_page_Entry(generator,
                               generator.mdvar._path['src_prefix'] +
                               call['paras']['src'],
                               call['target'])
        entries[page] = entry

        generator.mdvar._listinfo['in_list'] = True
        local_bk = generator.mdvar.local_backup()
        entry.processContext()
        generator.mdvar.update_local(entry.get_mdlocal())

        page_cached[call['paras']['dst']] = entry.meta['title']
        generator.mdvar.local_restore(local_bk)

    page_cached_all = copy.deepcopy(page_cached)
    page_cached_all['home'] = None

    for cur in page_cached_all:
        lines = []
        for dst in page_cached:
            if cur == dst:
                lines.append('<li class="nav-item">' +
                             '<a class="pure-button ' +
                             ' pure-button-disabled">' +
                             page_cached[dst] +
                             '</a></li>')
            else:
                lines.append('<li class="nav-item">' +
                             '<a class="pure-button" ' +
                             'href="' +
                             dst + '.html' +
                             '">' +
                             page_cached[dst] +
                             '</a></li>')

        if cur is 'home':
            generator.loaded['snippet'].templates['cover'] =\
                COVER.replace('to_be_replace','\n'.join(lines))
        else:
            generator.loaded['snippet'].templates[cur + '_cover'] =\
                COVER.replace('to_be_replace','\n'.join(lines))

    for page in pages:
        call = MiduHelper.parseVar(page)

        entry = entries[page]
        generator.mdvar._listinfo['in_list'] = True
        local_bk = generator.mdvar.local_backup()
        entry.processContext()
        generator.mdvar.update_local(entry.get_mdlocal())

        generator.generatePage(re.match('(.*)', page))
        generator.mdvar.local_restore(local_bk)


def get_page_Entry(generator, target, temp):
    if not target.endswith('.md'):
        target += '.md'

    parser_name = temp + 'parser'
    if parser_name in generator.default:
        module = generator.default[parser_name].split('.')
    else:
        return MDEntry.MDEntry(target, generator.mdvar)

    mod = generator.loaded['code'].get(module[0])
    klass = getattr(mod, module[1])
    if issubclass(klass, MDEntry.MDEntry):
        return klass(target, generator.mdvar)
    else:
        return MDEntry.MDEntry(target, generator.mdvar)
