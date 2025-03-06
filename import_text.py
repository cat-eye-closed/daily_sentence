def read_file_to_dict(filename):
    result = {}
    key = None
    value = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('# ') or line.startswith('## ') or line.strip() == '':
                continue

            if line.startswith('##### '):
                if key is not None:
                    result[int(key)] = ''.join(value).replace('\n', '<br>').strip()
                key = line.strip('#\n')
                value = []
            else:
                value.append(line)

        if key is not None and value:
            result[int(key)] = ''.join(value).replace('\n', '<br>').strip()

    return result
