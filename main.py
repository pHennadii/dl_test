import parser
import route_finder


def preprocess():
    tickets = parser.Parser.parse_data('data.xml')
    tickets.sort(key=lambda t: (t.dep_station_id, t.arr_station_id, t.dep_time))
    station_indexes = {}
    ind = 0
    for t in tickets:
        if t.dep_station_id not in station_indexes:
            station_indexes[t.dep_station_id] = ind
            ind += 1
        if t.arr_station_id not in station_indexes:
            station_indexes[t.arr_station_id] = ind
            ind += 1

    station_indexes_rev = dict(
        zip(
            list(station_indexes.values()),
            list(station_indexes.keys())
        )
    )

    adj_matrix = {}
    for t in tickets:
        if station_indexes[t.dep_station_id] not in adj_matrix:
            adj_matrix[station_indexes[t.dep_station_id]] = []
        adj_matrix[station_indexes[t.dep_station_id]].append((
            t.train_id,
            station_indexes[t.arr_station_id],
            t.price,
            t.dep_time,
            t.arr_time,
            station_indexes[t.dep_station_id])
        )
    return adj_matrix, station_indexes, station_indexes_rev


def main():
    adj_list, station_indexes, station_indexes_rev = preprocess()

    print("enter best way criteria (1 - cheapest, 2 - fastest)")
    criteria = int(input())

    print(f"enter start station (availible: {station_indexes.keys()})")
    start = station_indexes[int(input())]

    print(f"enter destination station (availible: {station_indexes.keys()})")
    dest = station_indexes[int(input())]

    rf = route_finder.RouteFinder(adj_list)

    if criteria == 1:
        path, cost = rf.find_cheapest_way(start, dest)
        path = [station_indexes_rev[st] for st in path]
        print("path: ", path, " cost: ", cost)
    elif criteria == 2:
        path, cost = rf.find_fastest_way(start, dest)
        path = [station_indexes_rev[st] for st in path]
        print("path: ", path, " time: ", cost)


if __name__ == "__main__":
    main()
