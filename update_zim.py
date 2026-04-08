import os
import re

import requests

WIKI_FOLDER = '.'


def compare_timestamp(t1, t2):
    t1 = t1.replace('-', '')
    t2 = t2.replace('-', '')
    return int(t1) - int(t2)


def check_zim(path):
    if result := re.findall(r'(.*?)_(.*?)_(.*)_(.*?).zim', path):
        name, lang, kind, timestamp = result[0]
    else:
        print('Error find name!', path)
        return None

    if name in ['wikispecies', 'minecraftwiki', 'zh.minecraft.wiki', 'bindingofisaacrebirth']:
        url = 'https://download.kiwix.org/zim/other'
    else:
        url = 'https://download.kiwix.org/zim/' + name

    while True:
        try:
            page = requests.get(url, timeout=10)
            break
        except Exception:
            continue

    content = page.content.decode('utf8')

    if result := re.findall(r'"(([^"]*?)_(.*?)_(.*)_(.*?).zim)".*(\d\d\d\d-\d\d-\d\d \d\d:\d\d)\s+(\S+)', content):
        latest = []
        current = None
        for zim in result:
            if (name, lang, kind) == zim[1:4]:
                if not latest or compare_timestamp(latest[4], zim[4]):
                    latest = zim
            if (name, lang, kind, timestamp) == zim[1:5]:
                current = zim

        if latest:
            if compare_timestamp(timestamp, latest[4]):
                print(path, '=>', 'Updated!', current[4:] if current else timestamp, '->', latest[4:])
                return url + '/' + latest[0]
            else:
                print(path, '=>', 'Already latest:', latest[4:])
                return None
        else:
            print('Error find latest!', path)
            return None
    else:
        print('Error find zim!', path)
        return None


def main():
    download = []
    for path in os.listdir(WIKI_FOLDER):
        if path.endswith('.zim'):
            if (path.startswith('wikihow') or path.startswith('wikipedia_en_for_schools')
                    or path.startswith('scp') or path.startswith('backrooms')):
                print(path)
            else:
                if zim := check_zim(path):
                    download.append(zim)

    for url in download:
        if url:
            print(url)
            print(url + '.sha256')


if __name__ == '__main__':
    main()
