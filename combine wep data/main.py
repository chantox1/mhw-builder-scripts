import json
import os, glob, errno

input_dir = 'in'
output_dir = 'out'

f_data = os.path.join(input_dir, 'wepDataBM.json')
with open(f_data) as f:
    wep_data_bm = json.load(f)

f_data = os.path.join(input_dir, 'wepDataGun.json')
with open(f_data) as f:
    wep_data_gun = json.load(f)

data = {
    "blade": wep_data_bm,
    "gun": wep_data_gun
}

f_out = os.path.join(output_dir, 'weapons.json')
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
