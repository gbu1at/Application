from SETTING import *
import json

with open(container_json_path, 'r') as f:
    data = json.load(f)

for x in data:
    if (x == "container"): continue
    print(data[x])
    for v in list(data[x]):
        vol = float(v) / 1000
        data[x][vol] = data[x][v]
        data[x].pop(v)
        data[x][vol]["volume"] = str(vol)

with open(container_json_path, 'w') as f:
    json.dump(data, f, ensure_ascii=False)
