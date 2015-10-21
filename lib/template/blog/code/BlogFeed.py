import time
import copy
import datetime


def get_feed(generator):
    tformat = "%Y-%m-%d %H:%M"

    res = []
    for md in generator.entry_cached:
        entries = generator.entry_cached[md][0]
        file_num_map = generator.entry_cached[md][1]

        for entry in entries.values():
            timestamp = time.mktime(datetime.
                                    datetime.
                                    strptime(entry.meta['date'], tformat).
                                    timetuple())
            meta = {}

            meta['action'] = "New post in " + generator.default['section']
            meta['date'] = entry.meta['date']
            meta['title'] = entry.meta['title']
            meta['section'] = generator.default['section']
            meta['description'] = entry.meta['description']
            blognum = file_num_map[entry.meta['md_filename']]
            meta['link'] = '${PREFIX}posts/blog' + str(blognum) + '.html'
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
               generator.mdvar._global['blogname'] +
               '</title>')
    rss.append('<link>' +
               prefix +
               '</link>')
    rss.append('<description>' +
               generator.mdvar._global['blogname'] +
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
