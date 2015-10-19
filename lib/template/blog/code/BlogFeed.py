import time
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
