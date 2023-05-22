import csv, json

f_data = 'in/data.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        ele1 = int(row['Element1'])
        ele1dmg = int(row['Element1Dmg'])
        ele2 = int(row['Element2'])
        ele2dmg = int(row['Element2Dmg'])
        new_row = {
            'Element1': ele1,
            'Element1Dmg': ele1dmg,
            'Element2': ele2,
            'Element2Dmg': ele2dmg
        }
        data[id] = new_row

f_out = 'out/dualEle.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
