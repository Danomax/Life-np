'''
RLE Run Length Encoding

2024 Aug Researcho

see LICENSE for copyrights
'''

import re

def encode(text: str) -> str:
    return re.sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1), text)

def decode(text):
    return re.sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)),
               text)

def rle_header(header):
    sets = header.split(',')
    x = int(re.search('[0-9]+',sets[0]).group())
    y = int(re.search('[0-9]+',sets[1]).group())
    rule = re.search('[bB][0-9]+[/][sS][0-9]+',sets[2]).group()
    return x,y,rule

def rle_open(rlefile):
    rlepattern = []
    with open(rlefile) as file:
        rlecode = ''
        for line in file:
            if line[0] != '#' and line[0] != 'x':
                rlecode += line.strip()
            elif line[0] == 'x':
                x, y, rule = rle_header(line)
    decodedrle = decode(rlecode)
    for s in decodedrle.split('$'):
        rlepattern.append(s)
    rlepattern[-1] = rlepattern[-1][:-1]
    return rlepattern, x, y, rule

'''
Test Code, uncomment to execute
text = '3o9b2$o3bo!'
text = text[:-1]
decodedtext = decode(text)
print(decodedtext)
print(encode(decodedtext))
'''