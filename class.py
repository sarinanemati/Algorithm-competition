import sys
from collections import defaultdict, deque

data = sys.stdin.read().strip().split('\n')

blocks = []
block = []
for line in data:
    if line.strip() == "":
        if block:
            blocks.append(block)
            block = []
    else:
        block.append(line.strip())
if block:
    blocks.append(block)

graph = defaultdict(list)
in_degree = defaultdict(int)
all_classes = set()

for block in blocks:
    header = block[0] 
    class_name = header.split()[1]
    all_classes.add(class_name)
    if 'extends' in header:
        parents = header.split('extends')[1].strip(" :").split(',')
        parents = [p.strip() for p in parents]
        for parent in parents:
            graph[parent].append(class_name)
            in_degree[class_name] += 1
            all_classes.add(parent)
            
for cls in all_classes:
    in_degree.setdefault(cls, 0)

queue = deque([cls for cls in all_classes if in_degree[cls] == 0])
topo_order = []

while queue:
    current = queue.popleft()
    topo_order.append(current)
    for neighbor in graph[current]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
if len(topo_order) == len(all_classes):
    print("possible")
else:
    print("impossible")
