import time
import copy
import datetime


IMG_ITEM = '''
<a class="example-image-link" href="${PREFIX}images/__img__" data-lightbox="__post-time__" data-title="__year____place__"><img class="example-image" src="${PREFIX}thumbs/thumb___img__" alt="__place__" /></a>
'''


def get_feed(generator):
    tformat = "%Y-%m-%d"

    res = []
    for md in generator.entry_cached:
        entries = generator.entry_cached[md][0]

        tmp_dict = {}
        for entry in entries.values():
            timestamp = time.mktime(datetime.
                                    datetime.
                                    strptime(entry.meta['post-time'], tformat).
                                    timetuple())
            if timestamp not in tmp_dict:
                tmp_dict[timestamp] = []
            tmp_dict[timestamp].append(entry)

        for timestamp in tmp_dict:
            meta = {}
            entry_list = tmp_dict[timestamp]

            meta['action'] = "New photos in " + generator.default['section']
            meta['date'] = entry_list[0].meta['post-time']
            places = []
            for entry in entry_list:
                places.append(entry.meta['place'])
            places = list(set(places))
            meta['title'] = ', '.join(places[:3]) + ' and so on'
            meta['section'] = generator.default['section']
            desc = []
            for entry in entry_list[:4]:
                img_item = copy.deepcopy(IMG_ITEM)
                img_item = img_item.replace('__year__', entry.meta['year'])
                img_item = img_item.replace('__img__', entry.meta['img'])
                img_item = img_item.replace('__place__', entry.meta['place'])
                img_item = img_item.replace('__post-time__', entry.meta['post-time'])
                desc.append(img_item)
            meta['description'] = '\n'.join(desc)
            meta['link'] = '${PREFIX}index.html'
            res.append((timestamp, meta))
    return res


RSS_HEAD = '''
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
'''
RSS_END = '''
</channel>
</rss>
'''


def produce_rss(generator):
    if 'rss_prefix' in generator.mdvar._global:
        prefix = generator.mdvar._global['rss_prefix']
        if not prefix.endswith('/'):
            prefix += '/'
    else:
        prefix = ''

    rss = [copy.deepcopy(RSS_HEAD)]
    rss.append('<title>' +
               generator.mdvar._global['camerarollname'] +
               '</title>')
    rss.append('<link>' +
               prefix +
               '</link>')
    rss.append('<description>' +
               generator.mdvar._global['camerarollname'] +
               '</description>')
    for item in sorted(get_feed(generator),
                       key=lambda x: x[0],
                       reverse=True)[:10]:
        rss.append('<item>')
        rss.append('<title>' + item[1]['title'] + '</title>')
        rss.append('<link>' + item[1]['link'] + '</link>')
        rss.append('<description>' + item[1]['description'] + '</description>')
        rss.append('</item>')

    rss.append(copy.deepcopy(RSS_END))

    fname = generator.mdvar._path['dst_prefix'] + 'rss.xml'
    content = '\n'.join(rss).replace('${PREFIX}', prefix).strip('\n')
    with open(fname, 'w') as f:
        f.write(content)
