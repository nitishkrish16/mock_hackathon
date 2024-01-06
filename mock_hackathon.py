import json

def find_minimum(route, places, distances, memo):
    min_distance = float('inf')
    place = -1

    for i, distance in enumerate(distances):
        if distance != 0 and i not in places:
            if min_distance > distance:
                place = i
                min_distance = distance
    
    route.append(min_distance)
    places.append(place)
    memo[tuple(places)] = min_distance

def solve(data):
    start_distance = data['restaurants']['r0']['neighbourhood_distance']
    all_distances = {'r0': start_distance}
    memo = {}

    for i in range(20):
        key = 'n' + str(i)
        distances = data['neighbourhoods'][key]['distances']
        all_distances[key] = distances
    
    route = []
    places = []
    
    find_minimum(route, places, all_distances['r0'], memo)
    
    for i in range(1, 21):
        if i == 1:
            find_minimum(route, places, all_distances['n0'], memo)
        else:
            last_place = places[-1]
            find_minimum(route, places, all_distances['n' + str(last_place)], memo)

    routes = {}
    total_cost = sum(route[-2::-1])
    

    for i in range(len(route)-1):
        val = 'n' + str(places[i])
        routes[val] = route[i]


    converted_path = ['r0'] + [f'n{place}' for place in places] + ['r0']
    converted_output = {"v0": {"path": converted_path}}

    with open('level0_output.json', "w") as json_file:
        json.dump(converted_output, json_file)
    
    return converted_output

# Load data from JSON file
with open('level0.json') as file:
    data = json.load(file)

# Solve the problem and output the result
converted_output = solve(data)
print(converted_output)
