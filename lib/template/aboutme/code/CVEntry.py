import MDEntry
from pybtex.database.input import bibtex


class CVEntry(MDEntry.MDEntry):
    def __init__(self, fname, mdvar):
        super(CVEntry, self).__init__(fname, mdvar)
        self.addHandler('bib', self.bib_handler)

    def bib_handler(self, matchobj):
        bib_file = matchobj.group(1)
        parser = bibtex.Parser()
        src = self.mdvar._path['src_prefix']
        bib_data = parser.parse_file(src + bib_file)

        bib_sorted = sorted(bib_data.entries.items(), cmp=sort_by_year)

        lines = []
        for key, value in bib_sorted:
            line = []
            authors = value.fields['author'].split('and')
            ref_authors = []
            for author in authors:
                ref_name = ''
                names = author.strip().split(' ')
                ref_name = names[0]
                if len(names) > 1:
                    ref_name += ' ' + names[1][0].upper() + '.'
                ref_authors.append(ref_name)
            if len(ref_authors) > 1:
                ref_authors[-1] = 'and ' + ref_authors[-1]
            line.append(', '.join(ref_authors))
            line.append('"' + value.fields['title'] + '"')
            line.append('In <em>' + value.fields['booktitle'] + '</em>,')
            line.append('pp. ' + value.fields['pages'] + '.')
            line.append(value.fields['organization'] + ',')
            line.append(value.fields['year'] + '.')
            lines.append(' '.join(line))
        return '\n'.join(lines)


def sort_by_year(y, x):
    return int(x[1].fields['year']) - int(y[1].fields['year'])
