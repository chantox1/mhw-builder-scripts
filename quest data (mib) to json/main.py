import json
import os
from decrypt import decrypt

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

BYTE_ORDER = 'little'
UINT32_MAX = 4294967295

def uint_from_bytes(buf, offset, size):
    return int.from_bytes(
        buf[offset: offset + size],
        byteorder='little'
    )

input_dir = 'in'
decrypted_dir = 'decrypted'
output_dir = 'out'

print('decrypting...')
decrypt(input_dir, decrypted_dir)

print('processing...')
data = {}
for fname in os.listdir(decrypted_dir):
    name, ext = os.path.splitext(fname)
    if ext != '.mib':
        continue

    fpath = os.path.join(decrypted_dir, fname)
    if not os.path.isfile(fpath):
        continue

    id = int(name[-5:])
    if id in dummy_quests:
        print(f'Skipping dummy quest with id {id}')
        continue

    with open(fpath, 'rb') as f:
        magic = f.read(4)
        buf = f.read()

    icons = []
    icon_offset = 68
    icon_block = 2
    for i in range(5):
        icon = uint_from_bytes(
            buf,
            icon_offset + i * icon_block,
            2
        )
        if icon == 127:
            continue
        icons.append(icon)

    monsters = []
    monster_offset = 172
    monster_block = 65
    for i in range(7):
        monster_id = uint_from_bytes(
            buf,
            monster_offset + i * monster_block,
            4
        )
        if monster_id == UINT32_MAX:
            continue
        monsters.append(monster_id)    

    entry = {
        'id': id,
        'index': len(data),
        'stars': buf[10],
        'monsters': monsters,
        'icons': icons
    }
    data[id] = entry

f_out = os.path.join(output_dir, 'quests.json')
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
