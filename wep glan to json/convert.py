import csv, json

f_data = 'in/data.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        shellId = int(row['ShellId'])
        shellLvl = int(row['ShellLvl']) + 1
        new_row = [shellId, shellLvl]
        data[id] = new_row

f_out = 'out/shelling.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
