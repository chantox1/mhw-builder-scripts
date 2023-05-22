import csv, json

f_data = 'in/data.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        set = int(row['Set'])
        color = int(row['Color'])
        new_row = {
            'Set': set,
            'Color': color
        }
        data[id] = new_row

f_out = 'out/skillColor.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
