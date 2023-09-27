import json
import os, sys, errno
import struct, readline0

dummy_quests = [
    # 'Unavailable'
    0,
    1,
    2,
    30000,
    30001,
    30002,
    30003,
    30004,
    30005,
    30006,
    30007,
    30008,
    30009,
    50831,
    51624,
    51625,

    # 'Invalid Message'
    3,
    4,
    5,
    50702,
    50992
]

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

data_names = {}
data_objectives = {}
for fname in os.listdir(input_dir):
    print(f'Parsing {fname}...')
    name, ext = os.path.splitext(fname)
    if ext != '.gmd':
        print(f'Warning: input file "{fname}" is not a .gmd file')
        continue

    fpath = os.path.join(input_dir, fname)
    if not os.path.isfile(fpath):
        continue

    id = int(name[1:6])
    if id in dummy_quests:
        print(f'Skipping dummy quest with id {id}')
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
        for count, line in enumerate(readline0.readline0(f)):
            strings[count] = cleanStr(line.decode('utf-8'), tag_map)

    lang = fname[-7:-4]
    if not lang in data_names:
        data_names[lang] = {}
    if not lang in data_objectives:
        data_objectives[lang] = {}

    id = int(name[1:6])
    data_names[lang][id] = strings[0]
    data_objectives[lang][id] = strings[1]

for lang in data_names:
    output_dir_lang = os.path.join(output_dir, lang)
    try:
        os.mkdir(output_dir_lang)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f_out = os.path.join(output_dir_lang, 'questNames.json')
    with open(f_out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_names[lang], ensure_ascii=False, separators=(',', ':')))

for lang in data_objectives:
    output_dir_lang = os.path.join(output_dir, lang)

    f_out = os.path.join(output_dir_lang, 'questObjectives.json')
    with open(f_out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_objectives[lang], ensure_ascii=False, separators=(',', ':')))
