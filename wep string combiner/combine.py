import json
import os, glob, errno

weps = {
    'GS': 0,
    'SnS': 1,
    'DB': 2,
    'LS': 3,
    'hammer': 4,
    'HH': 5,
    'lance': 6,
    'GL': 7,
    'SA': 8,
    'CB': 9,
    'IG': 10,
    'Bow': 11,
    'HBG': 12,
    'LBG': 13
}

input_dir = 'in'
output_dir = 'out'

f_data = os.path.join(input_dir, 'wepDataBM.json')
with open(f_data) as f:
    wep_data_bm = json.load(f)

f_data = os.path.join(input_dir, 'wepDataGun.json')
with open(f_data) as f:
    wep_data_gun = json.load(f)

_, dirs, _ = next(os.walk(input_dir))
for lang in dirs:
    data = {}

    cur_dir = os.path.join(input_dir, lang)
    _, _, files = next(os.walk(cur_dir))

    for file in files:
        f_in = os.path.join(cur_dir, file)
        with open(f_in, encoding='utf-8') as f:
            str_data = json.load(f)
        wepId = weps[os.path.splitext(file)[0]]

        data[wepId] = {}
        for _, val in (wep_data_bm if wepId < 11 else wep_data_gun)[str(wepId)].items():
            key = str(val['name'])
            if key in str_data:
                data[wepId][key] = str_data[key]
    
    output_dir_lang = os.path.join(output_dir, lang)
    try:
        os.mkdir(output_dir_lang)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f_out = os.path.join(output_dir_lang, 'wepNames.json')
    with open(f_out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))

    
