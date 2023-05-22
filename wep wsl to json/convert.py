import csv, json

f_data = 'in/data.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        notes = [int(x) for x in [
            row['Note_1'],
            row['Note_2'],
            row['Note_3']
        ]]
        new_row = notes
        data[id] = new_row

f_out = 'out/notes.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
