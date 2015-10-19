def get_feed(generator):
    res = {}
    for md in generator.entry_cached:
        entries = generator.entry_cached[md][0]
        for entry in entries:
            res[entry.meta['title']] = entry.meta['description']
    return res
