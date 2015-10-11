import os
import re
import glob
import shutil
import MiduHelper
import MDEntry


def copy_files(generator):
    src_f = generator.mdvar._path['src_prefix']
    dst_f = generator.mdvar._path['dst_prefix']

    if os.path.exists(src_f):
        for f in glob.glob(src_f + '*.jpg'):
            shutil.copy2(f, dst_f)


def generate_sidebar(generator):
    if 'pages' not in generator.mdvar._global:
        return

    pages = generator.mdvar._global['pages'].split(',')
    for page in pages:
        call = MiduHelper.parseVar(page)

        entry = get_page_Entry(generator,
                               generator.mdvar._path['src_prefix'] +
                               call['paras']['src'],
                               call['target'])

        local_bk = generator.mdvar.local_backup()
        entry.processContext()
        generator.mdvar.update_local(entry.get_mdlocal())

        generator.generatePage(re.match('(.*)', page))

        generator.mdvar.local_restore(local_bk)


def get_page_Entry(generator, target, temp):
    if not target.endswith('.md'):
        target += '.md'

    parser_name = temp + 'parset'
    if parser_name in generator.default:
        module = generator.default[parser_name].split('.')
    else:
        return MDEntry.MDEntry(target, generator.mdvar)

    mod = generator.loaded['code'].get(module[0])
    klass = getattr(mod, module[1])
    if issubclass(klass, MDEntry.MDEntry):
        return klass(target)
    else:
        return MDEntry.MDEntry(target, generator.mdvar)
