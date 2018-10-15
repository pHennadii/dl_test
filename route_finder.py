import datetime

INF = 100000000


class RouteFinder:
    def preprocess(self, start, adj_matrix, fn):
        used = {}
        optimal = {}

        for station in adj_matrix:
            used[station] = False
            optimal[station] = fn(INF)
        prev = [0] * len(used)
        tickets = [0] * len(used)
        optimal[start] = fn(0)

        return prev, used, tickets, optimal

    def cheapest_way(self, start: int, adj_matrix: dict):
        prev, used, tickets, optimal = self.preprocess(start, adj_matrix, int)

        for i in range(0, len(adj_matrix)):
            v = -1
            for j in range(0, len(adj_matrix)):
                if not used[j] and (v == -1 or optimal[j] < optimal[v]):
                    v = j
            if optimal[v] == INF:
                break
            used[v] = True
            for j in range(0, len(adj_matrix[v])):
                to = adj_matrix[v][j][1]
                cost = adj_matrix[v][j][2]
                # print(to, cost)
                if optimal[v] + cost < optimal[to]:
                    optimal[to] = optimal[v] + cost
                    tickets[to] = adj_matrix[v][j][0]
                    prev[to] = v

        return optimal, prev, tickets

    def timedelta(self, time1, time2: datetime.time):
        seconds1 = int(time1.second)
        seconds2 = int(time2.second)
        minutes1 = int(time1.minute)
        minutes2 = int(time2.minute)
        hours1 = int(time1.hour)
        hours2 = int(time2.hour)

        delta = hours2 * 3600 + minutes2 * 60 + seconds2 - \
                hours1 * 3600 - minutes1 * 60 - seconds1

        if delta < 0:
            delta += 86400

        return delta

    def fastest_way(self, start, adj_matrix):
        prev, used, tickets, optimal = self.preprocess(start, adj_matrix, datetime.timedelta)

        for i in range(0, len(adj_matrix)):
            v = -1
            for j in range(0, len(adj_matrix)):
                if not used[j] and (v == -1 or optimal[j] < optimal[v]):
                    v = j

            if optimal[v] == datetime.timedelta(INF):
                break
            used[v] = True
            for j in range(0, len(adj_matrix[v])):
                to = adj_matrix[v][j][1]
                timediff = self.timedelta(adj_matrix[v][j][4], adj_matrix[v][j][3])
                # print(to, timediff)
                if optimal[v] + datetime.timedelta(seconds=timediff) < optimal[to]:
                    optimal[to] = optimal[v] + datetime.timedelta(seconds=timediff)
                    tickets[to] = adj_matrix[v][j][0]
                    prev[to] = v

        return optimal, prev, tickets

    def find_fastest_way(self, start, dest, adj_matrix: dict):
        optimal, prev, tickets = self.fastest_way(start, adj_matrix)
        path = []
        time = datetime.timedelta(0)

        while dest != start:
            path.append(dest)
            time += optimal[dest]
            dest = prev[dest]

        path.append(start)
        path.reverse()
        return path, time

    def find_cheapest_way(self, start, dest: int, adj_matrix: dict):
        optimal, prev, tickets = self.cheapest_way(start, adj_matrix)
        path = []
        cost = 0.0

        while dest != start:
            path.append(dest)
            cost += optimal[dest]
            dest = prev[dest]

        path.append(start)
        path.reverse()
        return path, cost
