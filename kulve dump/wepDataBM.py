import csv, json
import os, errno

class TreeData:
    def _get_crt_data(self, fpath):
        data = {}
        for wep_type in range(0,14):
            data[wep_type] = {}
        with open(fpath, encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                wep_type = int(row['Class'])
                index = int(row['Index'])
                new_row = {
                    'Class': wep_type,
                }
                data[wep_type][index] = new_row
        return data
    
    def _get_cus_data(self, fpath):
        data = {}
        for wep_type in range(0,14):
            data[wep_type] = {}
        with open(fpath, encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                wep_type = int(row['Class'])
                index = int(row['Index'])
                tree_index = int(row['TreeIndex'])
                children = [int(x) for x in [
                    row['Child1'],
                    row['Child2'],
                    row['Child3'],
                    row['Child4']
                ]]
                new_row = {
                    'TreeIndex': tree_index,
                    'Class': wep_type,
                    'Children': children
                }
                data[wep_type][index] = new_row
        return data

    def __init__(self, crt_path, cus_path):
        self.create_data = self._get_crt_data(crt_path)
        self.upgrade_data = self._get_cus_data(cus_path)

    def _get_entry(self, data, wep_type, index):
        if index in data[wep_type]:
            return data[wep_type][index]
        return None
    
    def get_entries(self, wep_type, index):
        return [self._get_entry(self.create_data, wep_type, index),
                self._get_entry(self.upgrade_data, wep_type, index)]
    
    def upgrade_has_children(self, upgrade):
        return bool(sum(upgrade['Children']))
    
    def _get_wep_data_entry(self, wep_data, wep_type, tree_index):
        if not tree_index:
            return None

        index = 0
        for key, entry in self.upgrade_data[wep_type].items():
            if entry['TreeIndex'] == tree_index:
                index = key
        if index == 0:
            print(f"! Failed search with tree index {tree_index} !")
            return None

        for wep in wep_data[wep_type].values():
            if wep['Index'] == index:
                return wep
        return None

    def is_final(self, wep_data, wep_type, wep_id):
        wep = wep_data[wep_type][wep_id]
        wep_index = wep['Index']
        create, upgrade = self.get_entries(wep_type, wep_index)
        if wep['Rarity'] > 8:
            if upgrade is None:
                return True
            return not self.upgrade_has_children(upgrade)
        else:
            if upgrade is None:
                return True
            for c_index in upgrade['Children']:
                c_wep = self._get_wep_data_entry(wep_data, wep_type, c_index)
                if c_wep is not None and c_wep['Rarity'] < 9:
                    return False
            return True

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
}

safi_bases = [
    [23,30],
    [26,35],
    [25,34],
    [26,35],
    [27,34],
    [24,30],
    [25,31],
    [24,31],
    [21,26],
    [25,32],
    [24,30]
]

kulve_parts = [
    [7,8,13,14],
    [7,8,13,14],
    [7,8,13,14],
    [7,8,13,14],
    [5,6,11,12],
    [5,6,11,12],
    [7,8,13,14],
    [7,8,13,14],
    [5,6,11,12],
    [5,6,11,12],
    [5,6,11,12]
]

kulve_raw = [
    [70, 90],
    [90, 110],
    [90, 110],
    [70, 90],
    [70, 90],
    [90, 110],
    [80, 100],
    [70, 90],
    [80, 100],
    [70, 90],
    [70, 90]
]

kulve_ele = [
    [15, 9],
    [15, 12],
    [18, 12],
    [15, 12],
    [15, 9],
    [15, 12],
    [24, 12],
    [18, 12],
    [18, 12],
    [15, 12],
    [15, 12]
]

crt_path = os.path.join('tree_data', 'weapon_crt.csv')
cus_path = os.path.join('tree_data', 'weapon_cus.csv')
tree_data = TreeData(crt_path=crt_path, cus_path=cus_path)

input_dir = 'in'
with open(os.path.join(input_dir, 'wepStr.json')) as f:
    wep_str = json.load(f)

with open(os.path.join(input_dir, 'kire.json')) as f:
    kire = json.load(f)

data = {}
for fname in os.listdir(input_dir):
    fpath = os.path.join(input_dir, fname)
    if not os.path.isfile(fpath):
        continue
    wep, ext = os.path.splitext(fname)
    if ext == '.json':
        print('json file')
        continue
    wepId = weps[wep]
    data[wep] = {}
    with open(fpath, encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if int(row['Damage']) <= 0:  # Skip dummy weapons
                continue
            if int(row['BaseId']) == safi_bases[wepId][1]:
            # We only want 1 copy of the safi weps so we ignore half the models
                continue
            index = int(row['Index'])
            id = int(row['Id'])
            name = wep_str[str(wepId)][row['Name']]
            rare = int(row['Rarity']) + 1
            damage = int(row['Damage'])
            defense = int(row['Defense'])
            aff = int(row['Affinity'])
            element = int(row['Element'])
            elementDmg = int(row['ElementDmg'])
            hiddenEle = int(row['HiddenEle'])
            hiddenEleDmg = int(row['HiddenEleDmg'])
            sharpId = int(row['SharpId'])
            sharpStart = int(row['SharpStart'])

            if (int(row['Part1']) in kulve_parts[wepId] and rare > 8):
                damage += kulve_raw[wepId][rare//12]
                if (element != 0):
                    elementDmg += kulve_ele[wepId][element//6]
                if (hiddenEle != 0):
                    hiddenEleDmg += kulve_ele[wepId][element//6]
                defense += 20

            slot_keys = [
                'Slot1',
                'Slot2',
                'Slot3'
            ]
            slots=[]
            for key in slot_keys:
                size=int(row[key])
                if size > 0:
                    slots.append(size)

            wepVar1 = int(row['WepVar1'])
            wepVar2 = int(row['WepVar2'])
            skill = int(row['Skill'])

            new_row = {
                'Index': index,
                'Name': name,
                'Rarity': rare,
                'Damage': damage,
                'Defense': defense,
                'Affinity': aff,
                'Slots': slots,
                'WepVar1': wepVar1,
                'WepVar2': wepVar2,
                'Sharp': kire[str(sharpId)]['Bar'],
                'StartingSharpness': 150 + 50 * sharpStart,
            }

            if int(row['BaseId']) == -1:
                new_row['Unique'] = False
            elif int(row['BaseId']) == safi_bases[wepId][0]:
                new_row['Safi'] = True

            if element != 0:
                new_row['Element'] = element
                new_row['ElementDmg'] = elementDmg

            if hiddenEle != 0:
                new_row['HiddenEle'] = hiddenEle
                new_row['HiddenEleDmg'] = hiddenEleDmg

            if skill != 0:
                new_row['Skill'] = skill

            if (int(row['Part1']) in kulve_parts[wepId] and rare > 8):
                data[wep][id] = new_row

f_out = 'out/data.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
