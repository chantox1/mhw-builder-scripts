import csv, json

f_data = 'in/kire.csv'
data = {}
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        id = int(row['Id'])
        sharp = [int(x) for x in [
            row['Red'],
            row['Orange'],
            row['Yellow'],
            row['Green'],
            row['Blue'],
            row['White'],
            row['Purple']
        ]]
        new_row = {
            'Id': id,
            'Bar': sharp
        }
        data[id] = new_row

f_out = 'out/kire.json'
with open(f_out, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
