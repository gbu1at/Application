import csv
path = "test.csv"

with open(path, 'r') as f:
    r = csv.DictReader(f)
    reader = []
    for line in r:
        reader.append(line)

with open(path, 'w') as f:
    write = csv.DictWriter(f, fieldnames=['1', '2', '3'])
    write.writeheader()
    for line in reader:
        if line['1'] == '3':
            line['2'] = 1
        write.writerow(line)

'''
1,2,3
1,1,1
2,2,2
3,3,3
4,4,4
'''