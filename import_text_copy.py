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
                    result[int(key)] = ''.join(value).strip()
                key = line.strip('#\n')
                value = []
            else:
                value.append(line)

        if key is not None and value:
            result[int(key)] = ''.join(value).strip()

    return result

'''
dict = read_file_to_dict('sentence.md')
list1 = dict.keys()
SENTENCE_NUM = len(dict)
list2 = list(range(1, SENTENCE_NUM+1))
print(list(set(list2) - set(list1)))
'''