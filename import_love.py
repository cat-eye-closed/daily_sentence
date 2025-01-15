def read_love_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    numbers = []
    for line in lines:
        line = line.strip()
        if line:  # 判断行是否为空
            try:
                number = int(line)  # 尝试转换为整数
            except ValueError:
                continue  # 如果转换失败，忽略这一行
            numbers.append(number)
    return numbers

def write_love_to_file(numbers, filename):
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(str(number) + '\n')
