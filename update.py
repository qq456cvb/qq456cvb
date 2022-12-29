from pathlib import Path
from pyquery import PyQuery as pq
import re

# borrowed from https://github.com/simonw/simonw/blob/master/build_readme.py
def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


root = Path(__file__).parent.resolve()
if __name__ == '__main__':
    d = pq('https://qq456cvb.github.io/publications/')
    pub = d('div.archive')
    pub = pub('table:first')
    print(pub)
    print(pub.html())
    entries = []
    for item in pub('tr'):
        item = pq(pq(item)('tr')('td')[1])
        txt = item.text().split('\n')
        title = txt[0]
        conf = txt[2].replace(', ', '')
        links = item('a')
        link_entries = []
        for link in links:
            link = pq(link)
            link_entries.append([link.attr('href'), link.text()])
        entries.append([title, conf, link_entries])

    mds = ''
    for entry in entries[:10]:
        mds += '* '
        mds += '[**{}**] '.format(entry[1])
        mds += entry[0]
        mds += ' ('
        mds += '/'.join(['[{}]({})'.format(link[1], link[0]) for link in entry[2]])
        mds += ')\n'
    
    readme = root / "README.md"
    mds += '* ... More publications on my [Website](https://qq456cvb.github.io/publications/)'
    rewritten = replace_chunk(readme.open().read(), "pub", mds)
    readme.open("w").write(rewritten)