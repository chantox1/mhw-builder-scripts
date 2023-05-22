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

if len(sys.argv) == 2:
    fname_out = sys.argv[1]

    for fname in os.listdir(input_dir):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath):
            strings = {}
            with open(fpath, 'rb') as f:
                buf = f.read(40)
                key_count, str_count, key_block_size, str_block_size, name_size = struct.unpack("<IIIIIIIIII", buf)[5:]
                head_size = 40 + name_size + 1
                info_entry_size = key_count * 32
                bucket_size = 256 * 8
                str_offset = head_size + info_entry_size + bucket_size + key_block_size

                f.seek(str_offset)
                for (i, line) in enumerate(readline0.readline0(f)):
                    strings[i] = cleanStr(line.decode('utf-8'), tag_map)
            lang = fname[-7:-4]
            output_dir_lang = os.path.join(output_dir, lang)
            try:
                os.mkdir(output_dir_lang)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            
            f_out = os.path.join(output_dir_lang, fname_out)
            with open(f_out, 'w', encoding='utf-8') as f:
                f.write(json.dumps(strings, ensure_ascii=False, separators=(',', ':')))
else:
    print("Script failed, missing output file name.")
