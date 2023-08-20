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
            if wep['index'] == index:
                return wep
        return None

    def is_final(self, wep_data, wep_type, wep_id):
        wep = wep_data[wep_type][wep_id]
        wep_index = wep['index']
        create, upgrade = self.get_entries(wep_type, wep_index)
        if wep['rarity'] > 8:
            if upgrade is None:
                return True
            return not self.upgrade_has_children(upgrade)
        else:
            if upgrade is None:
                return True
            for c_index in upgrade['Children']:
                c_wep = self._get_wep_data_entry(wep_data, wep_type, c_index)
                if c_wep is not None and c_wep['rarity'] < 9:
                    return False
            return True

weps = {
    'Bow': 11,
    'HBG': 12,
    'LBG': 13
}

crt_path = os.path.join('tree_data', 'weapon_crt.csv')
cus_path = os.path.join('tree_data', 'weapon_cus.csv')
tree_data = TreeData(crt_path=crt_path, cus_path=cus_path)

input_dir = 'in'
data = {}
for fname in os.listdir(input_dir):
    fpath = os.path.join(input_dir, fname)
    if not os.path.isfile(fpath):
        continue
    wep, _ = os.path.splitext(fname)
    wepId = weps[wep]
    data[wepId] = {}
    with open(fpath, encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if int(row['Damage']) <= 0:  # Skip dummy weapons
                continue
            index = int(row['Index'])
            id = int(row['Id'])
            name = int(row['Name'])
            rare = int(row['Rarity']) + 1
            damage = int(row['Damage'])
            defense = int(row['Defense'])
            aff = int(row['Affinity'])
            element = int(row['Element'])
            elementDmg = int(row['ElementDmg'])
            hiddenEle = int(row['HiddenEle'])
            hiddenEleDmg = int(row['HiddenEleDmg'])

            # TODO: Kulve parts / upgrades

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

            skill = int(row['Skill'])
            deviation = int(row['Deviation'])
            specialAmmo = int(row['SpecialAmmo'])

            new_row = {
                'id': id,
                'index': index,
                'name': name,
                'rarity': rare,
                'attack': damage,
                'defense': defense,
                'affinity': aff,
                'slots': slots,
            }

            if int(row['BaseId']) != -1:
                new_row['unique'] = True
            # TODO: Safi parts

            if (wepId == 12):
                new_row['specialAmmo'] = specialAmmo

            if (wepId != 11):
                new_row['deviation'] = deviation

            data[wepId][id] = new_row

temp_data = data.copy()
for wep_type in range(11, 14):
    for wep_id in temp_data[wep_type]:
        if tree_data.is_final(data, wep_type, wep_id):
            data[wep_type][wep_id]['final'] = True

f_out = 'out/wepDataGun.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
