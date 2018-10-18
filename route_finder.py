import datetime


class RouteFinder:
    __INF = 100000000
    __adj_matrix = {}
    __start = -1

    __used = {}
    __optimal = {}
    __prev = []
    __tickets = []

    def __init__(self, adj_matrix: dict):
        self.__adj_matrix = adj_matrix.copy()

    def __preprocess(self, start, fn):
        self.__used = \
            dict(zip(list(self.__adj_matrix.keys()), [False]*len(self.__adj_matrix)))
        self.__optimal = \
            dict(zip(list(self.__adj_matrix.keys()), [fn(self.__INF)]*len(self.__adj_matrix)))

        self.__optimal[start] = fn(0)

        self.__prev = [0]*len(self.__used)
        self.__tickets = [0]*len(self.__used)

    def __cheapest_way(self, start: int):
        self.__preprocess(start, int)

        for i in range(0, len(self.__adj_matrix)):
            v = -1

            for j in range(0, len(self.__adj_matrix)):
                if not self.__used[j] and (v == -1 or self.__optimal[j] < self.__optimal[v]):
                    v = j

            if self.__optimal[v] == self.__INF:
                break

            self.__used[v] = True
            for j in range(0, len(self.__adj_matrix[v])):
                to = self.__adj_matrix[v][j][1]
                cost = self.__adj_matrix[v][j][2]
                # print(to, cost)
                if self.__optimal[v] + cost < self.__optimal[to]:
                    self.__optimal[to] = self.__optimal[v] + cost
                    self.__tickets[to] = self.__adj_matrix[v][j][0]
                    self.__prev[to] = v

    @staticmethod
    def __timedelta(time1, time2: datetime.time):
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

    def __fastest_way(self, start):
        self.__preprocess(start, datetime.timedelta)

        for i in range(0, len(self.__adj_matrix)):
            v = -1

            for j in range(0, len(self.__adj_matrix)):
                if not self.__used[j] and (v == -1 or self.__optimal[j] < self.__optimal[v]):
                    v = j

            if self.__optimal[v] == datetime.timedelta(self.__INF):
                break

            self.__used[v] = True

            for j in range(0, len(self.__adj_matrix[v])):
                to = self.__adj_matrix[v][j][1]
                timediff = self.__timedelta(self.__adj_matrix[v][j][4], self.__adj_matrix[v][j][3])

                if self.__optimal[v] + datetime.timedelta(seconds=timediff) \
                        < self.__optimal[to]:

                    self.__optimal[to] = self.__optimal[v] + \
                                         datetime.timedelta(seconds=timediff)
                    self.__tickets[to] = self.__adj_matrix[v][j][0]
                    self.__prev[to] = v

    def find_fastest_way(self, start, dest: int):
        if start != self.__start:
            self.__start = start
            self.__fastest_way(self.__start)

        path = []
        time = datetime.timedelta(0)

        while dest != start:
            path.append(dest)
            time += self.__optimal[dest]
            dest = self.__prev[dest]

        path.append(start)
        path.reverse()
        return path, time

    def find_cheapest_way(self, start, dest: int):
        if start != self.__start:
            self.__start = start
            self.__cheapest_way(self.__start)

        path = []
        cost = 0.0

        while dest != start:
            path.append(dest)
            cost += self.__optimal[dest]
            dest = self.__prev[dest]

        path.append(start)
        path.reverse()
        return path, cost
