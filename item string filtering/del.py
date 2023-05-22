import json
import os, glob, errno

input_dir = 'in'
output_dir = 'out'

whitelist=[
    '180', # Powercharm
    '182', # Powertalon
    '42',  # Demondrug
    '44',  # Mega Demondrug
    '40',  # Might seed
    '60',  # Demon powder
    '46',  # Might pill

    '184', # Armorcharm
    '186', # Armortalon
    '50',  # Armorskin
    '52',  # Mega armorskin
    '48',  # Adamant seed
    '62',  # Hardshell powder
    '54',  # Adamant pill
]

f_data = os.path.join(input_dir, 'decos.json')
with open(f_data) as f:
    deco_data = json.load(f)

for fpath in glob.iglob(input_dir + '**/**', recursive=True):
    if os.path.isfile(fpath) and os.path.splitext(fpath)[1] == '.json':
        if os.path.split(fpath)[1] != 'decos.json':
            with open(fpath, encoding='utf-8') as f:
                str_data = json.load(f)
            new_str_data = {}
            for deco in deco_data:
                id = deco['Name']
                if str(id) in str_data:
                    new_str_data[id] = str_data[str(id)]

            for id, string in str_data.items():
                if (id in whitelist) and (int(id) not in new_str_data):
                    new_str_data[int(id)] = string
            
            lang = fpath[3:6]
            output_dir_lang = os.path.join(output_dir, lang)
            try:
                os.mkdir(output_dir_lang)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            f_out = os.path.join(output_dir_lang, 'decoStr.json')
            with open(f_out, 'w', encoding='utf-8') as f:
                f.write(json.dumps(new_str_data, ensure_ascii=False, separators=(',', ':')))
