import csv, json
import os, sys, errno

tag_map = {
    "<ICON ALPHA>": " α",
    "<ICON BETA>": " β",
    "<ICON GAMMA>": " γ"
}

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

input_dir = 'in'
output_dir = 'out'

if len(sys.argv) == 2:
    fname_out = sys.argv[1]

    for fname in os.listdir(input_dir):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath):
            strings = {}
            with open(fpath, encoding='utf-8') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    id = row['Id']
                    string = handleTags(row['String'], tag_map)
                    strings[id] = string
            
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
