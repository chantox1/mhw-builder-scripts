import csv, json
import os

f_data = 'in/data.csv'
data = []
with open(f_data, encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for i, row in enumerate(csv_reader):
        data[i] = row

lang = ['ara', 'chS', 'chT', 'eng', 'fre', 'ger', 'ita', 'jpn', 'kor', 'pol', 'ptB', 'rus', 'spa']
for code in lang:
    f_strings = os.path.join('in', code, 'armorStr.json')
