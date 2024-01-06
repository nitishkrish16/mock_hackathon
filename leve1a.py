with open('/content/level1a.json') as file:
    data1 = json.load(file)

paths_i = []
def find_minimum(route, places, distances, memo):
    min_distance = float('inf')
    place = -1

    for i, distance in enumerate(distances):
        if distance != 0 and i not in places and str(i) in vertex_split:
            if min_distance > distance:
                place = i
                min_distance = distance
    
    route.append(min_distance)
    places.append(place)
    memo[tuple(places)] = min_distance


orders = {}

for i in range(20):
    key = 'n' + str(i)
    distances = data1['neighbourhoods'][key]['order_quantity']
    orders[key] = distances
ord = sorted(orders.items(), key=lambda x:x[1])
ord = ord[::-1]
print(ord)
while ord:
  max_capacity = data1["vehicles"]["v0"]["capacity"]
  vertices = []
  for a,b in ord:
    max_capacity-=b
    if max_capacity>=0:
      vertices.append(a)
    else:
      break

  vertex_split = []
  for i in vertices:
    vertex_split.append(i[1:3])
  vertices.insert(0,'r0')
  vertices.append('r0')
  print(vertex_split)
  start_distance = data1['restaurants']['r0']['neighbourhood_distance']
  all_distances = {'r0': start_distance}
  memo = {}
  for i in range(len(vertices)-1):
      if vertices[i]=='r0':
        distances = data1['restaurants'][vertices[i]]['neighbourhood_distance']
        all_distances[vertices[i]] = distances
      else:
        distances = data1['neighbourhoods'][vertices[i]]['distances']
        all_distances[vertices[i]] = distances

  route = []
  places = []
 # print(vertices)
  for i in range(len(vertices)):
    find_minimum(route, places, all_distances[vertices[i]], memo)
  routes = {}
 # print(route)
 # print(places)
  for i in range(len(route)-1):
      if places[i]!=-1:  
        #print(places[i])
        val = 'n' + str(places[i])
        routes[val] = route[i]

  converted_path = ['r0'] + [routes[val] for routes[val] in routes] + ['r0']
  converted_output = {"v0": {"path": converted_path}}
  
  paths_i.append(converted_output)
  ord = ord[len(vertex_split):]
  print(ord)

  from collections import defaultdict
node_dict = defaultdict(list)
for i, path in enumerate(paths_i, start=1):
    for key, value in path.items():
        node_dict[key].append(value['path'])

# Reformatting the paths
result = {}
for key, paths in node_dict.items():
    result[key] = {f"path{i}": path for i, path in enumerate(paths, start=1)}

with open('level1a_output.json', "w") as json_file:
    json.dump(result, json_file)