import os
from PIL import Image
from distutils import dir_util

size = (200, 200)


def generate(generator):
    src_dir = generator.mdvar._path['src_prefix'] + 'images'
    dst_dir = generator.mdvar._path['dst_prefix'] + 'images'
    thumb_dir = generator.mdvar._path['dst_prefix'] + 'thumbs'

    if os.path.exists(src_dir):
        dir_util.copy_tree(src_dir, dst_dir)

    if not os.path.exists(thumb_dir):
        os.mkdir(thumb_dir)

    for f in os.listdir(src_dir):
        im = Image.open(src_dir + '/' + f)
        w, h = im.size
        if w > h:
            new_length = h * 0.8
            new_size = (int(w/2 - new_length/2),
                        0,
                        int(w/2 + new_length/2),
                        int(new_length))
        else:
            new_length = w
            new_size = (0,
                        int(h/2 - new_length/2),
                        int(new_length),
                        int(h/2 + new_length/2))

        im = im.crop(new_size)
        im.thumbnail(size)
        im.save(thumb_dir + '/' + 'thumb_' + f)
