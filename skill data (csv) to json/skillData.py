import csv
import json

def unpack_row(row):
    id = int(row['Id'])
    lvl = int(row['Level'])
    params = [int(x) for x in [row['Param_5'], row['Param_6'], row['Param_7'], row['Param_8']]]

    u_id = [int(x) for x in [row['Unlock_Skill_1'], row['Unlock_Skill_2'], row['Unlock_Skill_3'],
                             row['Unlock_Skill_4'], row['Unlock_Skill_5'], row['Unlock_Skill_6']
    ]]
    u_lvl = [int(x) for x in [row['Unlock_Level_1'], row['Unlock_Level_2'], row['Unlock_Level_3'],
                              row['Unlock_Level_4'], row['Unlock_Level_5'], row['Unlock_Level_6']
    ]]
    unlock = []
    for i in range(6):
        unlock.append([u_id[i], u_lvl[i]])
    return id, lvl, params, unlock


def concat_data(row_i, data):
    id_i, lvl_i, params_i, unlock_i = unpack_row(row_i)

    name = 3*id_i
    desc = 3*id_i + 2

    new_row = { 'Name': name, 'Desc': desc, 'Max': lvl_i, 'Params': [[lvl_i] + params_i] }
    if sum([x[0] for x in unlock_i]) != 0:  # Means this skill entry requires a secret to activate
        print("Here!")
        new_row['Unlock'] = unlock_i

    for row in data:
        id, lvl, params, unlock = unpack_row(row)

        if id == id_i and lvl != lvl_i and lvl != 0:
            new_row['Params'].append([lvl] + params)
            if sum([x[0] for x in unlock]) == 0:
                if lvl > new_row['Max']:
                    new_row['Max'] = lvl
            else:
                if 'Unlock' not in new_row:
                    new_row['Unlock'] = unlock
                if 'MaxSecret' not in new_row or lvl > new_row['MaxSecret']:
                    new_row['MaxSecret'] = lvl

    param_sorter = lambda x : x[0]
    new_row['Params'].sort(key=param_sorter)  # Sort by level, just in case
    return new_row

f_data = 'in/data.csv'
data = []
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        data.append(row)

filtered_data = {}
for row in data:
    id = row['Id']
    if id not in filtered_data:
        new_row = concat_data(row, data)
        filtered_data[id] = new_row

f_out = 'out/skills.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False, separators=(',', ':')))
