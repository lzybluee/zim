import os

WIKI_FOLDER = '..'
SKIP_EXIST = True


def get_string(file):
    ret = bytearray()
    while True:
        content = file.read(1)
        if not content:
            print('Read EOF!')
            exit(0)
        if content[0] == 0:
            return ret.decode('utf8')
        ret.append(content[0])


def get_need_mime(file):
    index = 0
    while True:
        mime = get_string(file)
        if not mime:
            break
        if mime == 'text/html':
            print(mime, '=>', index)
            return index
        index += 1
    return 0


def read_zim(path, output_path):
    entry_list = []

    with open(os.path.join(WIKI_FOLDER, path), 'rb') as file:
        content = file.read(80)
        entry_count = int.from_bytes(content[24:28], 'little')
        url_offset = int.from_bytes(content[32:40], 'little')
        mime_offset = int.from_bytes(content[56:64], 'little')
        print('entryCount', entry_count)

        file.seek(mime_offset)
        need_mime = get_need_mime(file)

        for i in range(0, entry_count):
            file.seek(url_offset + 8 * i)
            content = file.read(8)
            entry_offset = int.from_bytes(content, 'little')
            file.seek(entry_offset)
            content = file.read(2)
            mime = int.from_bytes(content[:2], 'little')
            if mime != 65535:
                file.read(14)
                url = get_string(file)
                title = get_string(file)
                entry_list.append((mime, url, title))
            else:
                content = file.read(10)
                redirect = int.from_bytes(content[6:10], 'little')
                url = get_string(file)
                title = get_string(file)
                entry_list.append((mime, url, title, redirect))

    if len(entry_list) != entry_count:
        print('Mismatch', len(entry_list), 'vs.', entry_count)
        exit(0)

    with open(output_path, 'w', encoding='utf8') as index_file:
        for entry in entry_list:
            match entry:
                case mime, url, _:
                    if mime == need_mime:
                        index_file.write(url + '\n')
                case _, url, _, redirect:
                    redirect_mime, redirect_url, *rest = entry_list[redirect]
                    if redirect_mime == need_mime:
                        index_file.write(url + ' => ' + redirect_url + '\n')


def main():
    for path in os.listdir(WIKI_FOLDER):
        if path.endswith('.zim') and not (path.startswith('scp') or path.startswith('backrooms')):
            output_path = os.path.join(WIKI_FOLDER, path.replace('.zim', '.txt'))
            if not (SKIP_EXIST and os.path.exists(output_path)):
                print(path, '=>', 'Reading')
                read_zim(path, output_path)
            else:
                print(path, '=>', 'Skip')


if __name__ == '__main__':
    main()
