import parser
import route_finder
import datetime


def preprocess():
    tickets = parser.Parser.parse_data('data.xml')
    tickets.sort(key=lambda t: (t.dep_station_id, t.arr_station_id, t.dep_time, t.duration()))
    station_indexes = {}
    ind = 0
    for t in tickets:
        if t.dep_station_id not in station_indexes:
            station_indexes[t.dep_station_id] = ind
            ind += 1
        if t.arr_station_id not in station_indexes:
            station_indexes[t.arr_station_id] = ind
            ind += 1

    station_indexes_rev = {}
    for k in station_indexes:
        station_indexes_rev[station_indexes[k]] = k

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
    # for station in adj_list:
    #     print(f"{station}")
    #     for tkt in adj_list[station]:
    #         print(tkt)
    # min = datetime.timedelta(100000000)
    # m1 = datetime.timedelta(5000)
    # print(m1)
    # return

    print("enter best way criteria (1 - cheapest, 2 - fastest)")
    criteria = int(input())

    print(f"enter start station (availible: {station_indexes.keys()})")
    start = station_indexes[int(input())]

    print(f"enter destination station (availible: {station_indexes.keys()})")
    dest = station_indexes[int(input())]

    rf = route_finder.RouteFinder()

    if criteria == 1:
        path, cost = rf.find_cheapest_way(start, dest, adj_list)

        for i in range(0, len(path)):
            path[i] = station_indexes_rev[path[i]]

        print("path: ", path, " cost: ", cost)
    elif criteria == 2:
        path, cost = rf.find_fastest_way(start, dest, adj_list)

        for i in range(0, len(path)):
            path[i] = station_indexes_rev[path[i]]

        print("path: ", path, " time: ", cost)


if __name__ == "__main__":
    main()
