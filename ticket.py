import datetime


class Ticket:
    train_id = 0
    dep_station_id = 0
    arr_station_id = 0
    price = 0.0
    dep_time = datetime.time(0, 0)
    arr_time = datetime.time(0, 0)
    dep_time_str = ""
    arr_time_str = ""

    @staticmethod
    def default():
        return Ticket(0, 0, 0, 0, 0, 0)

    def duration(self):
        FMT = "%H:%M:%S"
        t1 = datetime.datetime.strptime(self.dep_time_str, FMT)
        t2 = datetime.datetime.strptime(self.arr_time_str, FMT)
        diff = t2-t1
        seconds = int(diff.seconds)
        if seconds < 0:
            seconds += 86400
        return seconds

    def __init__(self, t_id, dep_id, arr_id, pr, dep_t, arr_t):
        self.train_id = int(t_id)
        self.dep_station_id = int(dep_id)
        self.arr_station_id = int(arr_id)
        self.price = float(pr)
        self.dep_time = dep_t
        self.arr_time = arr_t

    def __str__(self):
        return f"train_id: {self.train_id} " \
               f"dep_station_id: {self.dep_station_id} " \
               f"arr_station_id: {self.arr_station_id} " \
               f"price: {self.price} " \
               f"dep_time: {self.dep_time} " \
               f"arr_time: {self.arr_time}"
