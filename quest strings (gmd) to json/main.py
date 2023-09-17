import json
import os, sys, errno
import struct, readline0

tag_map = {
    "<ICON ALPHA>": " α",
    "<ICON BETA>": " β",
    "<ICON GAMMA>": " γ"
}

def handleSpc(string):
    new_str = ""
    for c in string:
        if c == "\r":
            pass
        elif c == "\n":
            new_str += " "
        else:
            new_str += c
    return new_str

def handleTags(string, map):
    new_str = ""
    tag = ""
    open = False
    for c in string:
        if open:
            tag += c
            if c == '>':
                open = False
                new_tag = map.get(tag)
                new_str += tag if new_tag is None else new_tag
                tag = ""
        elif c == '<':
            tag += c
            open = True
        else:
            new_str += c
    return new_str

def cleanStr(string, tag_map):
    return handleTags(handleSpc(string), tag_map)

input_dir = 'in'
output_dir = 'out'

data = {}
for fname in os.listdir(input_dir):
    print(f'Parsing {fname}...')
    name, ext = os.path.splitext(fname)
    if ext != '.gmd':
        print(f'Warning: input file "{fname}" is not a .gmd file')
        continue

    fpath = os.path.join(input_dir, fname)
    if not os.path.isfile(fpath):
        continue

    strings = {}
    with open(fpath, 'rb') as f:
        buf = f.read(40)
        key_count, str_count, key_block_size, str_block_size, name_size = struct.unpack("<IIIIIIIIII", buf)[5:]
        head_size = 40 + name_size + 1
        info_entry_size = key_count * 32
        bucket_size = 256 * 8
        str_offset = head_size + info_entry_size + bucket_size + key_block_size

        f.seek(str_offset)
        for line in readline0.readline0(f):
            quest_name = cleanStr(line.decode('utf-8'), tag_map)
            break

    lang = fname[-7:-4]
    if not lang in data:
        data[lang] = {}

    id = int(name[1:6])
    data[lang][id] = quest_name

for lang in data:
    output_dir_lang = os.path.join(output_dir, lang)
    try:
        os.mkdir(output_dir_lang)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f_out = os.path.join(output_dir_lang, 'questNames.json')
    with open(f_out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data[lang], ensure_ascii=False, separators=(',', ':')))
