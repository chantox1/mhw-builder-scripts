import csv, json

f_data = 'in/data.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        name = int(row['Name Id'])
        rare = int(row['Rarity']) + 1
        type = int(row['Type'])
        stats = [int(x) for x in [
            row['Def'],
            row['Fire'],
            row['Water'],
            row['Ice'],
            row['Thunder'],
            row['Dragon']
        ]]

        set_skill = int(row['Set Skill Id']) if (int(row['Set Skill Level']) > 0) else -1

        skill_keys = [
            ['Skill Id 1', 'Skill Level 1'],
            ['Skill Id 2', 'Skill Level 2'],
            ['Skill Id 3', 'Skill Level 3']
        ]
        skills = []
        for key in skill_keys:
            s_id = int(row[key[0]])
            s_lvl = int(row[key[1]])
            if s_lvl > 0:
                skills.append([s_id, s_lvl])
        
        slot_keys = [
            'Size 1',
            'Size 2',
            'Size 3'
        ]
        slots=[]
        for key in slot_keys:
            size = int(row[key])
            if size > 0:
                slots.append(size)
        
        
        if (stats[0] != 0 or (type == 5 and name != 0)):
            new_row = {
                'Name': name,
                'Rarity': rare,
                'Type': type,
                'Stats': stats,
                'Skills': skills,
                'Slots': slots
            }
            if set_skill != -1:
                new_row['SetSkill'] = set_skill

            data[id] = new_row

f_out = 'out/data.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))

