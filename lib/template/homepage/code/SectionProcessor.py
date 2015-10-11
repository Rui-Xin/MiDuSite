import os
import glob
import shutil


def copy_files(generator):
    src_f = generator.mdvar._path['src_prefix']
    dst_f = generator.mdvar._path['dst_prefix']

    if os.path.exists(src_f):
        for f in glob.glob(src_f + '*.jpg'):
            shutil.copy2(f, dst_f)
